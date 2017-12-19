from ortools.constraint_solver import pywrapcp

from scheduler.models.classroom_m import ClassroomInfo
from scheduler.string_name import CLASSROOM, ID
from scheduler.util import str_to_list, list_to_str


def assign_to_different_time(data_list, week):

    solver = pywrapcp.Solver('time_scheduler')

    # 솔버 변수 선언
    sequence_data_list = list()
    for data in data_list:
        duration_var = solver.FixedDurationIntervalVar(data.get('range_from'),
                                                       data.get('range_to'),
                                                       data.get('duration'),
                                                       False,
                                                       "sub {}".format(data.get(ID)))
        # 각각의 범위 값들이 특정 값을 포함하지 않도록 제약
        classroom = data.get(CLASSROOM)
        avoid_date_string = classroom.schedule
        avoid_date_list = str_to_list(avoid_date_string)[week]
        try:
            for avoid in avoid_date_list:
                solver.Add(duration_var.AvoidsDate(avoid))
        except TypeError:
            pass
        sequence_data_list.append(duration_var)

    # 솔버 제약조건 추가 (최대 범위 내에서 데이터들이 겹치지 않도록 효율적으로 채우기)
    disjunctive_constraint = solver.DisjunctiveConstraint(sequence_data_list, 'duration')
    sequence_var = disjunctive_constraint.SequenceVar()
    solver.Add(disjunctive_constraint)
    print(data.EndExpr() for data in sequence_data_list)
    obj_var = solver.Max([data.EndExpr() for data in sequence_data_list])
    objective_monitor = solver.Minimize(obj_var, 1)

    # solver 가 풀어내는것에 대한 옵션
    sequence_phase = solver.Phase([sequence_var], solver.SEQUENCE_SIMPLE)
    vars_phase = solver.Phase([obj_var], solver.CHOOSE_RANDOM, solver.ASSIGN_RANDOM_VALUE)
    main_phase = solver.Compose([sequence_phase, vars_phase])

    # 솔류션 모음
    collector = solver.AllSolutionCollector()

    # Add the interesting variables to the SolutionCollector.
    collector.Add([sequence_var])
    collector.AddObjective(obj_var)

    for j in range(0, sequence_var.Size()):
        interval = sequence_var.Interval(j)
        collector.Add(interval.StartExpr().Var())
        collector.Add(interval.EndExpr().Var())

    # Solve the problem.
    if solver.Solve(main_phase, [objective_monitor, collector]):
        solution_num = 0
        sequence = collector.ForwardSequence(solution_num, sequence_var)
        seq_size = len(sequence)

        schedule_dict = dict()

        for j in range(0, seq_size):
            t = sequence_var.Interval(sequence[j])
            st = collector.Value(solution_num, t.StartExpr().Var())
            en = collector.Value(solution_num, t.EndExpr().Var())
            data = data_list[sequence[j]]
            classroom = data[CLASSROOM]
            if schedule_dict.get(classroom.id) is None:
                schedule_dict[classroom.id] = [t for t in range(st, en + 1)]
            else:
                schedule_dict[classroom.id] = schedule_dict.get(classroom.id) + [t for t in range(st, en + 1)]
            data['start_time'] = st
            data['end_time'] = en
        for i in schedule_dict.keys():
            classroom = ClassroomInfo.objects.get(id=i)
            list_data = str_to_list(classroom.schedule)
            list_data[week] = list_data[week] + schedule_dict.get(i)
            classroom.schedule = list_to_str(list_data)
            classroom.save()
