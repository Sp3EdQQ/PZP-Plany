import {University} from "../../types/University.ts";

type SideBarRightProps = {
    faculty: University[string] | undefined;
    teachers: string[];
};

export const SideBarRight = ({faculty, teachers}: SideBarRightProps) => {
    return (
        <>
            {faculty && (
                <div className="bg-white rounded-xl p-6 shadow-md w-4/5 max-h-screen overflow-auto">
                    <h2 className="text-xl text-center font-bold text-black mb-4">
                        Wszyscy nauczyciele
                    </h2>
                    {teachers.length > 0 ? (
                        <ul className="space-y-2">
                            {teachers.map((teacher, index) => (
                                <li key={teacher} className="text-black text-center">
                                    {teacher}
                                    {index < teachers.length - 1 && <hr className="border-custom-blue my-2"/>}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-center text-gray-600">Brak nauczycieli</p>
                    )}
                </div>
            )}
        </>
    );
};
