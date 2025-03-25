import {useState} from "react";
import {Classes} from "@/components/classes/Classes.tsx";
import {SideBarRight} from "@/components/SideBarRight.tsx";
import {University} from "../../types/University.ts";

type MainContentProps = {
    propSelectedWydzial: string;
    propData: University;
};

export const MainContent = ({propSelectedWydzial, propData}: MainContentProps) => {
    const faculty = propData[propSelectedWydzial];
    const [selectedCatedral, setSelectedCatedral] = useState<string | null>(null);

    const getTeachersByCatedral = (catedral: string | null) => {
        if (!faculty || !catedral) return [];
        return Object.keys(faculty[catedral] || {}).sort();
    };

    const teachers = getTeachersByCatedral(selectedCatedral);
    const showSidebar = faculty && teachers.length > 0; // Sprawdza, czy sidebar powinien być widoczny

    return (
        <div className="relative w-4/5 p-5 overflow-x-hidden min-h-screen flex flex-row justify-center">
            <div
                className="absolute inset-0 bg-cover bg-center bg-no-repeat brightness-50 z-0"
                style={{backgroundImage: "url('/bg.png')", backgroundAttachment: "fixed"}}
            ></div>

            {/* Main Content */}
            <div className={`${showSidebar ? "w-2/3" : "w-full"} pr-5 relative z-10`}>
                <h1 className="text-center p-5 text-5xl text-white font-bold">Plany UBB</h1>
                <div>
                    {faculty ? (
                        Object.keys(faculty).length > 0 ? (
                            Object.keys(faculty).map((catedral) => {
                                const displayCatedral = catedral.trim() === "" ? "Nienazwane" : catedral;
                                return (
                                    <Classes
                                        key={catedral}
                                        propCatedral={displayCatedral}
                                        dataCatedral={catedral}
                                        propSelectedWydzial={propSelectedWydzial}
                                        propData={propData}
                                        isOpen={selectedCatedral === catedral}
                                        onToggle={() =>
                                            setSelectedCatedral(selectedCatedral === catedral ? null : catedral)
                                        }
                                    />
                                );
                            })
                        ) : (
                            <div className="text-center text-white">Brak katedr</div>
                        )
                    ) : (
                        <div className="text-center text-white">
                            <div className="text-xl font-semibold">Witaj na stronie Plany UBB</div>
                            <div>Kliknij po lewej stronie na wydział, aby wyszukać katedry.</div>
                        </div>
                    )}
                </div>
            </div>

            {/* Sidebar Right - renderowany tylko jeśli jest potrzebny */}
            {showSidebar && (
                <div className="relative z-10 w-1/3 flex justify-end pr-3">
                    <SideBarRight faculty={faculty} teachers={teachers}/>
                </div>
            )}
        </div>
    );
};
