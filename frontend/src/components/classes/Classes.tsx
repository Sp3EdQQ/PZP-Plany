import {useState} from "react";
import {getGroups} from "@/components/classes/GroupSelector.ts";
import {getStudyTypeLabel, getStudyTypes} from "@/components/classes/StudyTypeSelector.ts";

const extractMajor = (groupString) => {
    return groupString.split("/")[0]; // Pobiera tylko nazwę kierunku
};

export const Classes = ({
                            propCatedral,
                            dataCatedral,
                            propSelectedWydzial,
                            propData,
                            isOpen,
                            onToggle
                        }) => {
    const [selectedType, setSelectedType] = useState<string | null>(null);
    const [selectedMajor, setSelectedMajor] = useState<string | null>(null);
    const [selectedGroup, setSelectedGroup] = useState<string | null>(null);

    const zajecia = propData?.[propSelectedWydzial]?.[dataCatedral] || {};
    const availableMajors = new Set<string>();
    const availableGroups = new Set<string>();
    const groupedBySubject: Record<string, Record<string, { rooms: string[] }>> = {};

    Object.entries(zajecia).forEach(([nauczyciel, zajeciaList]) => {
        zajeciaList.forEach((zaj) => {
            const studyType = zaj.groups.length ? getStudyTypes().find(type => zaj.groups.some(g => g.includes(`/${type}/`))) ?? "S" : "S";
            if (selectedType && studyType === selectedType) {
                zaj.groups.forEach(groupString => {
                    const major = extractMajor(groupString);
                    availableMajors.add(major);
                    if (selectedMajor === major) {
                        const groups = getGroups([groupString]);
                        groups.forEach(group => availableGroups.add(group));
                        if (!selectedGroup || groups.includes(selectedGroup)) {
                            const subject = zaj.subject || "Nienazwane";
                            if (!groupedBySubject[subject]) groupedBySubject[subject] = {};
                            if (!groupedBySubject[subject][nauczyciel]) groupedBySubject[subject][nauczyciel] = {rooms: []};
                            groupedBySubject[subject][nauczyciel].rooms.push(...zaj.rooms);
                        }
                    }
                });
            }
        });
    });

    return (
        <div className="my-4">
            <div
                className={`bg-white text-black flex justify-center w-3/5 mx-auto p-4 cursor-pointer rounded-xl text-lg font-semibold shadow-md transition-all duration-300 hover:scale-105 hover:bg-gray-200 ${isOpen ? "scale-110 !bg-custom-blue !text-white" : ""}`}
                onClick={onToggle}>
                {propCatedral}
            </div>
            {isOpen && (
                <div className="p-6 flex flex-col items-center">
                    <div className="flex gap-4 mb-4">
                        {getStudyTypes().map((type) => (
                            <button key={type}
                                    className={`bg-white text-black px-6 py-2 rounded-lg font-semibold transition-all duration-300 shadow-md hover:scale-105 hover:bg-gray-200 cursor-pointer ${selectedType === type ? "scale-110 !bg-custom-blue !text-white" : ""}`}
                                    onClick={() => {
                                        setSelectedType(type === selectedType ? null : type);
                                        setSelectedMajor(null);
                                        setSelectedGroup(null);
                                    }}>
                                {getStudyTypeLabel(type)}
                            </button>
                        ))}
                    </div>
                    {selectedType && availableMajors.size > 0 && (
                        <div className="flex gap-4 mb-4">
                            {[...availableMajors].map((major) => (
                                <button key={major}
                                        className={`bg-white text-black px-6 py-2 rounded-lg font-semibold transition-all duration-300 shadow-md hover:scale-105 cursor-pointer hover:bg-gray-200 ${selectedMajor === major ? "scale-110 !bg-custom-blue !text-white" : ""}`}
                                        onClick={() => {
                                            setSelectedMajor(major === selectedMajor ? null : major);
                                            setSelectedGroup(null);
                                        }}>
                                    {major}
                                </button>
                            ))}
                        </div>
                    )}
                    {selectedMajor && availableGroups.size > 0 && (
                        <div className="flex gap-4 mb-4">
                            {[...availableGroups].map((group) => (
                                <button key={group}
                                        className={`bg-white text-black px-6 py-2 rounded-lg font-semibold transition-all duration-300 shadow-md hover:scale-105 cursor-pointer hover:bg-gray-200 ${selectedGroup === group ? "scale-110 !bg-custom-blue !text-white" : ""}`}
                                        onClick={() => setSelectedGroup(group === selectedGroup ? null : group)}>
                                    {group}
                                </button>
                            ))}
                        </div>
                    )}
                    {selectedMajor && selectedType && Object.keys(groupedBySubject).length > 0 ? (
                        <div className="grid grid-cols-2 gap-6">
                            {Object.entries(groupedBySubject).map(([subject, teachers]) => (
                                <div key={subject} className="bg-white text-black p-6 rounded-xl shadow-md w-80">
                                    <h2 className="text-xl text-center font-bold border-b border-black pb-2 mb-2">{subject}</h2>
                                    <ul className="space-y-2">
                                        {Object.entries(teachers).map(([nauczyciel, {rooms}], index) => (
                                            <li key={index} className="text-center">
                                                <p className="font-semibold">{nauczyciel}</p>
                                                <p className="text-sm text-gray-600">Sala: {rooms.join(", ")}</p>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    ) : (
                        selectedMajor && selectedType &&
                        <p className="text-center text-gray-500">Brak zajęć dla wybranego kierunku lub grupy.</p>
                    )}
                </div>
            )}
        </div>
    );
};