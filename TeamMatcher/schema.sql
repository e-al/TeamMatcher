-- Entities --
DROP DATABASE IF EXISTS `teammatcher$TeamMatcher`;
CREATE DATABASE `teammatcher$TeamMatcher`;

USE `teammatcher$TeamMatcher`;

CREATE TABLE Class(
	    Class_Id int(11) AUTO_INCREMENT PRIMARY KEY,
    	Name varchar(100)
    	);

CREATE TABLE Project(
        Project_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Name varchar(100),
	    Description varchar(255),
        Max_Capacity int(11),
        Status varchar(100),
        Team_Name varchar(100)
        );


CREATE TABLE ProjectCategory(
        Project_Category_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Name varchar(100)
        );


CREATE TABLE Skill(
        Skill_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Name varchar(100)
    	);


CREATE TABLE Student(
        Student_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Email varchar(100),
        Password varchar(100),
        Name varchar(100),
        School varchar(100),
        Year  year(4),
        Major varchar(100),
        GPA decimal(10,0),
        Likes int(11)
        );


CREATE TABLE Team(
        Team_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Name varchar(100)
        );


-- Relationships --

CREATE TABLE ProjectBelongsToCategory(
        Project_Belongs_To_Category_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Project_Id int(11),
        Project_Category_Id int(11),
    	FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id),
        FOREIGN KEY (Project_Category_Id) REFERENCES ProjectCategory(Project_Category_Id)
    	);


CREATE TABLE ProjectForClass(
        Project_For_Class_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Project_Id int(11),
        Class_Id int(11),
    	FOREIGN KEY (Project_Id) REFERENCES Project(Project_Id),
        FOREIGN KEY (Class_Id) REFERENCES Class(Class_Id)
        );


CREATE TABLE StudentEnrolledInClass(
        Student_Enrolled_In_Class_Id int(11) PRIMARY KEY,
        Student_Id int(11),
        Class_Id int(11),
        FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
        FOREIGN KEY (Class_Id) REFERENCES Class(Class_Id)
        );


CREATE TABLE StudentHasSkill(
        Student_Has_Skill_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Skill_Level int(11),
        Student_Id int(11),
        Skill_Id int(11),
        FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
        FOREIGN KEY (Skill_Id) REFERENCES Skill(Skill_Id)
        );


CREATE TABLE StudentPartOfTeam(
        Student_Part_Of_Team_Id int(11) AUTO_INCREMENT PRIMARY KEY,
    	Student_Id int(11),
        Team_Id int(11),
        FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
        FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id)
        );

CREATE TABLE AvailableTime(
        Available_Time_Id int(11) AUTO_INCREMENT PRIMARY KEY,
        Team_Id int(11),
        Student_Id int(11),
        Dow int(11)
            check(DOW >= 0 and number <= 6),
        Start int(11)
            check(Start >= 0 and Start <= 23),
        Until int(11)
             check(Start >= 0 and Start <= 23),
    	FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id),
        FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id)
        );
