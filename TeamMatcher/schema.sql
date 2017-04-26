-- Entities --
DROP DATABASE IF EXISTS `teammatcher$TeamMatcher`;
CREATE DATABASE `teammatcher$TeamMatcher`;

USE `teammatcher$TeamMatcher`;

CREATE TABLE Class (
    Class_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Name     VARCHAR(100)
);

CREATE TABLE Student (
    Student_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Email      VARCHAR(100),
    Password   VARCHAR(100),
    Name       VARCHAR(100),
    School     VARCHAR(100),
    Year       INT(4),
    Major      VARCHAR(100),
    GPA        FLOAT(3, 2),
    Likes      INT(11)
);

CREATE TABLE Project (
    Project_Id         INT(11)               AUTO_INCREMENT PRIMARY KEY,
    Name               VARCHAR(100),
    Description        VARCHAR(5000),
    Max_Capacity       INT(11),
    Status             VARCHAR(100) NOT NULL DEFAULT 'Created',
    Team_Id            INT(11),
    CreatedByStudentId INT(11),
    FOREIGN KEY (CreatedByStudentId) REFERENCES Student (Student_Id) ON DELETE CASCADE
);

CREATE TABLE ProjectCategory (
    Project_Category_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Name                VARCHAR(100)
);


CREATE TABLE Skill (
    Skill_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Name     VARCHAR(100)         UNIQUE
);


-- Relationships --

CREATE TABLE ProjectBelongsToCategory (
    Project_Belongs_To_Category_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Project_Id                     INT(11),
    Project_Category_Id            INT(11),
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE,
    FOREIGN KEY (Project_Category_Id) REFERENCES ProjectCategory (Project_Category_Id) ON DELETE CASCADE
);


CREATE TABLE ProjectForClass (
    Project_For_Class_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Project_Id           INT(11),
    Class_Id             INT(11),
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE,
    FOREIGN KEY (Class_Id) REFERENCES Class (Class_Id) ON DELETE CASCADE
);

CREATE TABLE ProjectNeedsSkill (
    Project_Needs_Skill_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Project_Id           INT(11),
    Skill_Id             INT(11),
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE,
    FOREIGN KEY (Skill_Id) REFERENCES Skill (Skill_Id) ON DELETE CASCADE
);

CREATE TABLE StudentEnrolledInClass (
    Student_Enrolled_In_Class_Id INT(11) PRIMARY KEY,
    Student_Id                   INT(11),
    Class_Id                     INT(11),
    FOREIGN KEY (Student_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE,
    FOREIGN KEY (Class_Id) REFERENCES Class (Class_Id) ON DELETE CASCADE
);


CREATE TABLE StudentHasSkill (
    Student_Has_Skill_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Skill_Level          INT(11),
    Student_Id           INT(11),
    Skill_Id             INT(11),
    FOREIGN KEY (Student_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE,
    FOREIGN KEY (Skill_Id) REFERENCES Skill (Skill_Id) ON DELETE CASCADE
);


CREATE TABLE StudentPartOfProject (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Student_Id              INT(11),
    Project_Id                 INT(11),
    FOREIGN KEY (Student_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE,
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE
);

CREATE TABLE AvailableTime (
    Available_Time_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Project_Id           INT(11),
    Student_Id        INT(11),
    Dow               INT(11)
        CHECK (DOW >= 0 AND number <= 6),
    Start             INT(11)
        CHECK (Start >= 0 AND Start <= 23),
    Until             INT(11)
        CHECK (Start >= 0 AND Start <= 23),
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE,
    FOREIGN KEY (Student_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE
);


-- Relationships for messaging --

CREATE TABLE Room (
    Room_Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255)
);

CREATE TABLE RoomMember (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Room_Id INT(11),
    Student_Id INT(11),
    FOREIGN KEY (Room_Id) REFERENCES Room (Room_Id) ON DELETE CASCADE,
    FOREIGN KEY (Student_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE
);

CREATE TABLE Message (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Recv_Room_Id INT(11),
    Sender_Id INT(11),
    Text VARCHAR(1000),
    Ts TIMESTAMP,
    FOREIGN KEY (Recv_Room_Id) REFERENCES Room (Room_Id) ON DELETE CASCADE,
    FOREIGN KEY (Sender_Id) REFERENCES Student (Student_Id) ON DELETE CASCADE
);

CREATE TABLE LastReadMessage (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Student_Id INT(11),
    Room_Id INT(11),
    Last_Msg_Id INT(11),
    Last_Read_Msg_Id INT(11),
    FOREIGN KEY (Room_Id) REFERENCES Room (Room_Id) ON DELETE CASCADE,
    FOREIGN KEY (Last_Msg_Id) REFERENCES Message (Id) ON DELETE CASCADE,
    FOREIGN KEY (Last_Read_Msg_Id) REFERENCES Message (Id) ON DELETE CASCADE,
    UNIQUE KEY (Student_Id, Room_Id)
);

CREATE TABLE RoomToProject (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Room_Id INT(11),
    Project_Id INT(11),
    FOREIGN KEY (Room_Id) REFERENCES Room (Room_Id) ON DELETE CASCADE,
    FOREIGN KEY (Project_Id) REFERENCES Project (Project_Id) ON DELETE CASCADE,
    UNIQUE KEY (Room_Id, Project_Id)
);

CREATE TABLE PrivateRoom (
    Id INT(11) AUTO_INCREMENT PRIMARY KEY,
    Room_Id INT(11),
    Combined_Users_Key VARCHAR(255),
    FOREIGN KEY (Room_Id) REFERENCES Room (Room_Id) ON DELETE CASCADE,
    UNIQUE KEY (Combined_Users_Key)
);