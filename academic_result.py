import csv


def make_report_card(courses_file, students_file, tests_file, marks_file):

    with open(students_file) as studentFile:
        students = csv.reader(studentFile, delimiter=',')
        students_dict = {}
        firstline = True
        for row in students:
            if firstline:
                firstline = False
                continue
            else:
                students_dict[int(row[0])] = row[1]
    with open(courses_file) as courseFile:
        courses = csv.reader(courseFile, delimiter=',')
        courses_dict = {}
        firstline = True
        for row in courses:
            if firstline:
                firstline = False
                continue
            else:
                courses_dict[int(row[0])] = [row[1], row[2], {}]
    with open(tests_file) as examFile:
        tests = csv.reader(examFile, delimiter=',')
        tests_dict = {}
        firstline = True
        for row in tests:
            if firstline:
                firstline = False
                continue
            else:
                courses_dict[int(row[1])][2][int(row[0])] = int(row[2])
                tests_dict[int(row[0])] = [int(row[1]), int(row[2])]

    with open(marks_file) as marksFile:
        marks = csv.reader(marksFile, delimiter=',')
        marks_dict = {}
        firstline = True
        for row in marks:
            if firstline:
                firstline = False
                continue
            else:
                if int(row[1]) in marks_dict.keys():
                    marks_dict[int(row[1])].extend([int(row[0]), int(row[2])])
                else:
                    marks_dict[int(row[1])] = [int(row[0]), int(row[2])]

    stud_marks = {}
    for student_id in marks_dict.keys():
        x = 0
        while x < len(marks_dict[student_id]):
            test_id = marks_dict[student_id][x]
            course_id = tests_dict[test_id][0]
            ct_grade = marks_dict[student_id][x+1] * tests_dict[test_id][1]/100
            if student_id in stud_marks:
                stud_marks[student_id].extend([course_id, test_id, ct_grade])
                x += 2
            else:
                stud_marks[student_id] = [course_id, test_id, ct_grade]
                x += 2

    stud_fmarks = {}
    for student_id in stud_marks.keys():
        x = 0
        grade = stud_marks[student_id][2]
        while x < len(stud_marks[student_id]):
            if x+5 < len(stud_marks[student_id]) and stud_marks[student_id][x] == stud_marks[student_id][x+3]:
                grade += stud_marks[student_id][x+5]
                x += 3
            else:
                if student_id in stud_fmarks:
                    stud_fmarks[student_id].extend(
                        [stud_marks[student_id][x], round(grade, 2)])
                    x += 3
                    if x < len(stud_marks[student_id]):
                        grade = stud_marks[student_id][x+2]
                else:
                    stud_fmarks[student_id] = [
                        stud_marks[student_id][x], round(grade, 2)]
                    x += 3
                    if x < len(stud_marks[student_id]):
                        grade = stud_marks[student_id][x+2]

    averages = {}
    for student in stud_fmarks.keys():
        total = 0
        x = 1
        y = 0
        while x < len(stud_fmarks[student]):
            total += stud_fmarks[student][x]
            x += 2
            y += 1
        average = round(total/y, 2)
        averages[student] = average

    res = open('Academic report.txt', 'w')
    line = "ACADEMIC RESULT OF STUDENTS-2022 \n\n"
    res.write(line)
    for student in stud_fmarks.keys():
        line = 'Student Id: {0}, name: {1}\n'.format(student, students_dict[student])
        res.write(line)
        line = 'Total Average: {0}%\n\n'.format(averages[student])
        res.write(line)
        x = 0
        while x < len(stud_fmarks[student]):
            cname = courses_dict[stud_fmarks[student][x]][0]
            tname = courses_dict[stud_fmarks[student][x]][1]
            line = 'Course: {0}, Teacher: {1}\n'.format(cname, tname)
            res.write(line)
            fgrade = stud_fmarks[student][x+1]
            line = 'Final Grade: {0}%\n\n'.format('{:.2f}'.format(fgrade))
            res.write(line)
            x += 2
    res.close()


make_report_card('courses.csv', 'students.csv', 'tests.csv', 'marks.csv')
