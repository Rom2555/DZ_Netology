from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):

        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.get_average_grade():.1f}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка. Сравнить можно только студента со студентом.'
        else:
            return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка. Сравнить можно только студента со студентом.'
        else:
            return self.get_average_grade() == other.get_average_grade()

    def get_average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        if all_grades:
            return sum(all_grades) / len(all_grades)
        else:
            return 0

    def add_finished_courses(self, course_name):
        if course_name not in self.finished_courses:
            self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(grade, int) or grade < 1 or grade > 10:
            return 'Ошибка. Оценка должна быть от 1 до 10.'

        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
                return None
            else:
                lecturer.grades[course] = [grade]
                return None
        else:
            return 'Ошибка. Студент может поставить оценку только лектору.'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.get_average_grade():.1f}')

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка. Сравнить можно только лектора с лектором.'
        else:
            return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка. Сравнить можно только лектора с лектором.'
        else:
            return self.get_average_grade() == other.get_average_grade()

    def get_average_grade(self):
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        if all_grades:
            return sum(all_grades) / len(all_grades)
        else:
            return 0


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')

    def rate_hw(self, student, course, grade):
        if not isinstance(grade, int) or grade < 1 or grade > 10:
            return 'Ошибка. Оценка должна быть от 1 до 10.'

        if isinstance(student,
                      Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
                return None
            else:
                student.grades[course] = [grade]
                return None
        else:
            return 'Ошибка. Ревьювер может поставить оценку только студенту.'


def get_student_course_average_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    else:
        return 0


def get_lecturer_course_average_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    else:
        return 0


# Тесты:

# Создаем студентов
student_1 = Student('Иван', 'Андреев', 'мужской')
student_2 = Student('Андрей', 'Иванов', 'мужской')

# Создаем лекторов
lecturer_1 = Lecturer('Ирина', 'Сергеева')
lecturer_2 = Lecturer('Мария', 'Сидорова')

# Создаем ревьюверов
reviewer_1 = Reviewer('Олег', 'Александров')
reviewer_2 = Reviewer('Алексей', 'Петров')

# Создаем менторов
mentor_1 = Mentor('Михаил', 'Михайлов')
mentor_2 = Mentor('Вася', 'Васильев')

# Добавляем курсы студентам
student_1.courses_in_progress += ['Python', 'Git']
student_2.courses_in_progress += ['Python', 'SQL']

# Добавляем курсы лекторам
lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2.courses_attached += ['Python', 'SQL']

# Добавляем курсы ревьюверам
reviewer_1.courses_attached += ['Python', 'Git']
reviewer_2.courses_attached += ['Python', 'SQL']

# Добавляем пройденные курсы студентам
student_1.add_finished_courses("C++")
student_2.add_finished_courses("C++")
student_2.add_finished_courses("Java")

# Ревьюверы делают оценки студентам
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Git', 8)

reviewer_2.rate_hw(student_2, 'Python', 9)
reviewer_2.rate_hw(student_2, 'SQL', 7)
reviewer_2.rate_hw(student_2, 'SQL', 8)

# Студенты делают оценки лекторам
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)

student_2.rate_lecture(lecturer_2, 'Python', 9)
student_2.rate_lecture(lecturer_2, 'SQL', 8)

# Вывод людей
print("Студент 1:")
print(student_1)
print("\nСтудент 2:")
print(student_2)
print("\nЛектор 1:")
print(lecturer_1)
print("\nЛектор 2:")
print(lecturer_2)
print("\nРевьювер 1:")
print(reviewer_1)
print("\nРевьювер 2:")
print(reviewer_2)

# Сравнение студентов
print("\nСравнение студентов:")
print("student_1 < student_2:", student_1 < student_2)
print("student_1 == student_2:", student_1 == student_2)
print("student_1 != student_2:", student_1 != student_2)
print("student_1 > student_2:", student_1 > student_2)
print("student_1 >= student_2:", student_1 >= student_2)
print("student_1 <= student_2:", student_1 <= student_2)

# Сравнение лекторов
print("\nСравнение лекторов:")
print("lecturer_1 < lecturer_2:", lecturer_1 < lecturer_2)
print("lecturer_1 == lecturer_2:", lecturer_1 == lecturer_2)
print("lecturer_1 != lecturer_2:", lecturer_1 != lecturer_2)
print("lecturer_1 > lecturer_2:", lecturer_1 > lecturer_2)
print("lecturer_1 >= lecturer_2:", lecturer_1 >= lecturer_2)
print("lecturer_1 <= lecturer_2:", lecturer_1 <= lecturer_2)

# Подсчёт средней оценки студентов по курсу Python
course = 'Python'
average_rating_student = get_student_course_average_grade([student_1, student_2], course)
print(f"\nСредняя оценка студентов по курсу '{course}': {average_rating_student:.2f}")

# Подсчёт средней оценки лекторов по курсу Git
course = 'Git'
average_rating_lecturer = get_lecturer_course_average_grade([lecturer_1, lecturer_2], course)
print(f"Средняя оценка лекторов по курсу '{course}': {average_rating_lecturer:.2f}")
