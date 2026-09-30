def main():
    n, k, m = map(int, input().split())

    semester_students = {}
    students = []

    for _ in range(n):
        data = input().split()

        enrollment = data[0]
        name = data[1]
        semester = int(data[2])
        cpi = float(data[3])
        marks = tuple(map(int, data[4:4 + m]))
        avg_marks = sum(marks) / m

        student = (enrollment, name, semester, cpi, marks, avg_marks)
        students.append(student)

        if semester not in semester_students:
            semester_students[semester] = []

        semester_students[semester].append(student)

    for semester in sorted(semester_students.keys()):
        ranked_students = sorted(
            semester_students[semester],
            key=lambda x: (-x[3], -x[5], x[0])
        )

        top_k = ranked_students[:k]

        print(
            f"Semester {semester}:",
            *[student[0] for student in top_k]
        )

    for subject_index in range(m):
        highest_mark = -1
        toppers = []

        for student in students:
            enrollment = student[0]
            marks = student[4]
            mark = marks[subject_index]

            if mark > highest_mark:
                highest_mark = mark
                toppers = [enrollment]

            elif mark == highest_mark:
                toppers.append(enrollment)

        toppers.sort()
        print(f"S{subject_index + 1}:", *toppers)


if __name__ == "__main__":
    main()
