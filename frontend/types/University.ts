type Department = {
    [subject: string]: string[];
};

type Faculty = {
    [department: string]: Department;
};

export type University = {
    [faculty: string]: Faculty;
};