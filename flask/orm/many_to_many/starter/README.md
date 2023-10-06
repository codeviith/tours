# Models

 - Student
    - id:         Integer (primary key)
    - fname:      String (not null)
    - lname:      String (not null)
    - grad_year:  Integer (not null)
 - Enrollment
    - id          Integer (primary key)
    - student_id: Integer (foreign key --> Student.id) 
    - course_id:  Integer (foreign key --> Course.id) 
    - term:       String (not null)
 - Course
    - id:         Integer (primary key)
    - title:       String (unqiue, not null)
    - instructor: String 
    - credits:    Integer
# Validation

  - Student
    - `grad_year` must be current year or greater
  - Enrollment
    - `term` must be a string that starts with 'S' or 'F' followed by digits \
  - Course
    - `name` must not be an empty string
# Routes

  - GET /students
  - GET /students/<int:id>
  - PATCH /students/<int:id>
  - DELETE /students/<int:id>
  - GET /students/<int:id>/courses
  - POST /students/<int:id>/enrollments
  - POST /students

# Response Formats

  - GET /students
  ```json
    [
        {
            id
            fname
            lname
            grad_year
            
    ]
  ```
  - GET /students/<int:id>
  ```json
      {
          id
          fname
          lname
          grad_year
          enrollments: [
                {
                    id
                    student_id
                    course_id
                    term
                    course {
                        id
                        name
                        instructor
                        credits
                    }
                }
            ]
        }
      }
  ```
  - PATCH /students/<int:id>
  ```json
      {
          id
          fname
          lname
          grad_year
      }
  ```

  - DELETE /students/<int:id>
  ```json
      {}
  ```
  - GET /students/<int:id>/courses
  ```json
    [
        {
            id
            name
            instructor
            credits
        }
    ]

  ```
  - POST /students/<int:id>/enrollments
  ```json
      {
          id
          student_id
          course_id
          term
          course {
            id
            name
            instructor
            credits
          }
      }
  ```