"""
Домашнее задание 'ООП, наследование, инкапсуляция и полиморфизм'. Егоров Роман, группа pd-136
"""

from functools import total_ordering


class GetAverageMixin:
    def get_average_grade(self):
        """
        Вычисляет среднюю оценку лектора по всем курсам.

        Returns:
            float: Средняя оценка. Если оценок нет, то 0.
        """
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0


class Grader:
    """
    Базовый класс для объектов, которые могут выставлять оценки.
    """

    def rate(self, target, course, grade):
        """
        Выставляет оценку другому участнику за курс.

        Args:
            target (object): Объект, которому ставится оценка.
            course (str): Название курса.
            grade (int): Оценка от 1 до 10.

        Returns:
            None: Если всё прошло успешно.
            str: Сообщение об ошибке.
        """
        if not isinstance(grade, int) or grade < 1 or grade > 10:
            return 'Ошибка. Оценка должна быть от 1 до 10.'

        # Проверяем, что у self есть courses_attached и target — courses_in_progress
        if hasattr(self, 'courses_attached') and hasattr(target, 'courses_in_progress'):
            if course not in self.courses_attached:
                return f'Ошибка: {self.name} не закреплён за курсом "{course}".'
            if course not in target.courses_in_progress:
                return f'Ошибка: {target.name} не проходит курс "{course}".'

        # Добавляем оценку
        if course in target.grades:
            target.grades[course].append(grade)
            return None
        else:
            target.grades[course] = [grade]
            return None


@total_ordering
class Student(GetAverageMixin, Grader):
    """
    Класс для студента.

    Атрибуты:
        name (str): Имя студента.
        surname (str): Фамилия студента.
        gender (str): Пол студента.
        finished_courses (list): Список завершённых курсов.
        courses_in_progress (list): Список курсов, которые проходит студент.
        grades (dict): Словарь оценок по курсам.
    """

    def __init__(self, name, surname, gender):
        """
        Инициализирует экземпляр класса Student.

        Args:
            name (str): Имя студента.
            surname (str): Фамилия студента.
            gender (str): Пол студента.
        """
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.courses_attached = []
        self.grades = {}

    def __str__(self):
        """
        Возвращает строковое представление экземпляра класса Student.

        Returns:
            str: Информация о студенте.
        """
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.get_average_grade():.1f}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}'
        )

    def __lt__(self, other):
        """
        Сравнивает студента с другим студентом по средней оценке.

        Args:
            other (Student): Другой студент для сравнения.

        Returns:
            bool
        """
        if not isinstance(other, Student):
            raise TypeError("Нельзя сравнивать студента с другим типом")
        return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        """
        Проверяет, равны ли средние оценки двух студентов.

        Args:
            other (Student): Другой студент для сравнения.

        Returns:
            bool
        """
        if not isinstance(other, Student):
            raise TypeError("Нельзя сравнивать студента с другим типом")
        return self.get_average_grade() == other.get_average_grade()

    def rate_lecture(self, lecturer, course, grade):
        """
        Позволяет студенту поставить оценку лектору за лекцию.

        Args:
            lecturer (Lecturer): Лектор, которому ставится оценка.
            course (str): Название курса.
            grade (int): Оценка от 1 до 10.

        Returns:
            None: Если всё прошло хорошо.
            str: Сообщение об ошибке.
        """
        return self.rate(lecturer, course, grade)


class Mentor:
    """
    Класс для менторов. Родительский класс для лекторов и ревьюеров.

    Атрибуты:
        name (str): Имя ментора.
        surname (str): Фамилия ментора.
        courses_attached (list): Список курсов ментора.
    """

    def __init__(self, name, surname):
        """
        Инициализирует экземпляр класса Mentor.

        Args:
            name (str): Имя ментора.
            surname (str): Фамилия ментора.
        """
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor, GetAverageMixin):
    """
    Класс для лектора.

    Атрибуты:
        name (str): Имя лектора.
        surname (str): Фамилия лектора.
        courses_attached (list): Список курсов лектора.
        grades (dict): Словарь оценок от студентов.
    """

    def __init__(self, name, surname):
        """
        Инициализирует экземпляр класса Lecturer.

        Args:
            name (str): Имя лектора.
            surname (str): Фамилия лектора.
        """
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        """
        Возвращает строковое представление экземпляра класса Lecturer.

        Returns:
            str: Информация о лекторе.
        """
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.get_average_grade():.1f}'
        )

    def __lt__(self, other):
        """
        Сравнивает лектора с другим лектором по средней оценке.

        Args:
            other (Lecturer): Другой лектор для сравнения.

        Returns:
            bool: True, если текущий лектор имеет меньшую среднюю оценку.
        """
        if not isinstance(other, Lecturer):
            raise TypeError("Нельзя сравнивать лектора с другим типом")
        return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        """
        Проверяет, средние оценки двух лекторов равны?

        Args:
            other (Lecturer): Другой лектор для сравнения.

        Returns:
            bool: True, если средние оценки равны.
        """
        if not isinstance(other, Lecturer):
            raise TypeError("Нельзя сравнивать лектора с другим типом")
        return self.get_average_grade() == other.get_average_grade()


class Reviewer(Mentor, Grader):
    """
    Класс ревьювера.

    Атрибуты:
        name (str): Имя ревьювера.
        surname (str): Фамилия ревьювера.
        courses_attached (list): Список курсов, за которыми закреплён ревьювер.
    """

    def __init__(self, name, surname):
        """
        Инициализирует экземпляр класса Reviewer.

        Args:
            name (str): Имя ревьювера.
            surname (str): Фамилия ревьювера.
        """
        super().__init__(name, surname)

    def __str__(self):
        """
        Возвращает строковое представление объекта Reviewer.

        Returns:
            str: Информация о ревьювере.
        """
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}'
        )

    def rate_hw(self, student, course, grade):
        """
        Выставляет оценку студенту за домашнюю работу.

        Args:
            student (Student): Студент, которому ставится оценка.
            course (str): Название курса.
            grade (int): Оценка от 1 до 10.

        Returns:
            None: Если всё ОК.
            str: Сообщение об ошибке.
        """
        return self.rate(student, course, grade)


def get_student_course_average_grade(students, course):
    """
    Вычисляет среднюю оценку всех студентов по конкретному курсу.

    Args:
        students (list): Список студентов.
        course (str): Название курса.

    Returns:
        float: Средняя оценка по курсу. 0, если оценок нет.
    """
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    return sum(all_grades) / len(all_grades) if all_grades else 0


def get_lecturer_course_average_grade(lecturers, course):
    """
    Вычисляет среднюю оценку всех лекторов по конкретному курсу.

    Args:
        lecturers (list): Список лекторов.
        course (str): Название курса.

    Returns:
        float: Средняя оценка по курсу. 0, если оценок нет.
    """
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    return sum(all_grades) / len(all_grades) if all_grades else 0


# Тесты
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

# Вывод информации
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

print("\nПроверка работы rate() и обработки ошибок:")

# Тест 1: Неверная оценка (меньше 1)
print("\nТест 1: Оценка меньше 1")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_attached = ['Python']
student_1.courses_in_progress = ['Python']
lecturer_1.courses_attached = ['Python']
result = student_1.rate(lecturer_1, 'Python', 0)
print("Результат:", result)  # Ожидаем: "Ошибка. Оценка должна быть от 1 до 10."

# Тест 2: Неверная оценка (больше 10)
print("\nТест 2: Оценка больше 10")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_attached = ['Python']
student_1.courses_in_progress = ['Python']
lecturer_1.courses_attached = ['Python']
result = student_1.rate(lecturer_1, 'Python', 11)
print("Результат:", result)  # Ожидаем: "Ошибка. Оценка должна быть от 1 до 10."

# Тест 3: Студент не закреплён за курсом
print("\nТест 3: Студент не закреплён за курсом")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_in_progress = ['Python']
lecturer_1.courses_attached = ['Python']
result = student_1.rate(lecturer_1, 'Python', 10)
print("Результат:", result)  # Ожидаем: "Ошибка: Иван не закреплён за курсом 'Python'."

# Тест 4: Лектор не преподает курс
print("\nТест 4: Лектор не преподает курс")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_attached = ['Python']
student_1.courses_in_progress = ['Python']
lecturer_1.courses_attached = ['Git']  # Не Python
result = student_1.rate(lecturer_1, 'Python', 10)
print("Результат:", result)  # Ожидаем: "Ошибка: Ирина Сергеева не закреплён за курсом 'Python'."

# Тест 5: Студент не проходит курс
print("\nТест 5: Студент не проходит курс")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_attached = ['Python']
lecturer_1.courses_attached = ['Python']
result = student_1.rate(lecturer_1, 'Python', 10)
print("Результат:", result)  # Ожидаем: "Ошибка: Иван Андреев не проходит курс 'Python'."

# Тест 6: Успешное выставление оценки
print("\nТест 6: Успешное выставление оценки")
student_1 = Student('Иван', 'Андреев', 'мужской')
lecturer_1 = Lecturer('Ирина', 'Сергеева')
student_1.courses_attached = ['Python']
student_1.courses_in_progress = ['Python']
lecturer_1.courses_attached = ['Python']
result = student_1.rate(lecturer_1, 'Python', 10)
print("Результат:", result)  # Ожидаем: None
print("Оценки лектора теперь:", lecturer_1.grades)