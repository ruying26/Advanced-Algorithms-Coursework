# An arrow A -> B means A is a prerequisite of B.

class Graph:
    def __init__(self):
        # A dictionary stores each vertex and its outgoing connections.
        # Example: {"A": ["B"], "B": []} means A -> B.
        self.edges = {}

    def addVertex(self, vertex):
        if vertex not in self.edges:
            self.edges[vertex] = []

    def addEdge(self, start, end):
        # Add the vertices first, then connect start -> end.
        self.addVertex(start)
        self.addVertex(end)
        if end not in self.edges[start]:
            self.edges[start].append(end)

    def listIncomingAdjacentVertex(self, vertex):
        result = []
        # Find all vertices that point TO the selected vertex.
        for start in self.edges:
            if vertex in self.edges[start]:
                result.append(start)
        return result


class Course:
    def __init__(self, code, name, credits, level):
        # Save the information belonging to this course.
        self.code = code
        self.name = name
        self.credits = credits
        self.level = level


# Create five Course objects.
courses = {
    "CS101": Course("CS101", "Introduction to Programming", 3, "Core"),
    "CS201": Course("CS201", "Data Structures", 3, "Core"),
    "CS301": Course("CS301", "Algorithms", 3, "Core"),
    "CS302": Course("CS302", "Database Systems", 3, "Elective"),
    "CS401": Course("CS401", "Software Engineering", 4, "Core")
}

# Use course codes as vertices. The Graph class does not need to know
# anything about course names, credits or levels, so it is reusable.
graph = Graph()
for code in courses:
    graph.addVertex(code)

# The FIRST course is a prerequisite of the SECOND course.
graph.addEdge("CS101", "CS201")
graph.addEdge("CS101", "CS301")
graph.addEdge("CS201", "CS301")
graph.addEdge("CS201", "CS302")
graph.addEdge("CS301", "CS401")
graph.addEdge("CS302", "CS401")

# Repeat the menu until the user chooses 5.
while True:
    print("\n--- Course Prerequisite System ---")
    print("1. View all courses")
    print("2. View course details")
    print("3. View prerequisites")
    print("4. View unlocked courses")
    print("5. Exit")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        # Compulsory (a): display every course name.
        for code in courses:
            print(code, "-", courses[code].name)

    elif choice in ["2", "3", "4"]:
        # Remove extra spaces and change lowercase letters to uppercase.
        code = input("Enter course code: ").strip().upper()

        if code not in courses:
            print("Course not found.")
            continue  # Go back to the menu.

        course = courses[code]

        if choice == "2":
            # Compulsory (b): show every detail, even for electives.
            print("Code:", course.code)
            print("Name:", course.name)
            print("Credit hours:", course.credits)
            print("Level:", course.level)

        elif choice == "3":
            # Compulsory (c): incoming connections are prerequisites.
            prerequisites = graph.listIncomingAdjacentVertex(code)
            print("Prerequisites for", course.name)
            if prerequisites == []:
                print("No prerequisites.")
            for prerequisite in prerequisites:
                print(prerequisite, "-", courses[prerequisite].name)

        elif choice == "4":
            # Compulsory (d): outgoing connections are unlocked courses.
            unlocked = graph.edges[code]
            print("Courses unlocked by", course.name)
            if unlocked == []:
                print("No courses unlocked.")
            for next_code in unlocked:
                print(next_code, "-", courses[next_code].name)

    elif choice == "5":
        print("Goodbye!")
        break  # Stop the menu loop and end the program.

    else:
        print("Invalid choice. Enter 1 to 5.")
