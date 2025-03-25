export type University = {
    [faculty: string]: Department;
};

export type Department = {
    [catedral: string]: TeacherClasses;
};

export type TeacherClasses = {
    [teacher: string]: ClassDetails[];
};

export type ClassDetails = {
    subject: string;
    activity_type: string;
    groups: string[];
    rooms: string[];
};
