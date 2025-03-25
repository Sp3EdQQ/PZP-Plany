import {University} from "../../types/University.ts"; // Zakładam, że ścieżka jest taka sama

type SideBarRightProps = {
    faculty: University[string] | undefined; // Typ dla faculty (obiekt wydziału lub undefined)
    teachers: string[];                      // Lista nauczycieli
};

export const SideBarRight = ({faculty, teachers}: SideBarRightProps) => {
    return (
        <>
            {faculty && (
                <div className="bg-white rounded-xl p-4 shadow-md w-90 h-full">
                    <h2 className="text-xl text-center font-bold text-black mb-4">Wszyscy nauczyciele</h2>
                    {teachers.length > 0 ? (
                        <ul className="space-y-2">
                            {teachers.map((teacher) => (
                                <li key={teacher} className="text-black text-center">
                                    {teacher}
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