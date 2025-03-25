import {useState} from "react";
import {Calendar} from "@/components/ui/calendar";
import {University} from "../../types/University.ts";

type SideBarLeftProps = {
    propData: University | null;
    propSetSelectedWydzial: (wydzial: string) => void;
};

export const SideBarLeft = ({propData, propSetSelectedWydzial}: SideBarLeftProps) => {
    const [date, setDate] = useState<Date | undefined>(new Date());
    const [activeWydzial, setActiveWydzial] = useState<string | null>(null);

    return (
        <div className="w-1/5 flex flex-col p-6 h-screen rounded">
            <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                className="rounded-md border w-64 bg-white text-black mx-auto shadow-md"
                classNames={{
                    day_selected: "bg-custom-blue text-white hover:bg-custom-blue hover:text-white focus:bg-custom-blue focus:text-white",
                }}
            />
            <div className="pt-4 px-4 flex flex-col gap-4">
                {propData &&
                    Object.keys(propData).map((wydzial) => (
                        <div
                            key={wydzial}
                            onClick={() => {
                                propSetSelectedWydzial(wydzial);
                                setActiveWydzial(wydzial);
                            }}
                            className={`bg-white text-black text-center rounded-xl py-3 px-5 cursor-pointer transition-all duration-300 hover:scale-105 hover:bg-gray-200 shadow-md ${
                                activeWydzial === wydzial
                                    ? "scale-110 bg-custom-blue"
                                    : ""
                            }`}
                        >
                            {wydzial}
                        </div>
                    ))}
            </div>
        </div>
    );
};