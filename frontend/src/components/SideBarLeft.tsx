import {useState} from "react"
import {Calendar} from "@/components/ui/calendar"
import {University} from "../../types/University.ts";

type SideBarLeftProps = {
    propData: University | null;
    propSetSelectedWydzial: (wydzial: string) => void;
};

export const SideBarLeft = ({propData, propSetSelectedWydzial}: SideBarLeftProps) => {
    const [date, setDate] = useState<Date | undefined>(new Date())

    return (<div className="w-1/5 flex-col m-6">
        <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            className="rounded-md border w-64"
        />
        <div className="pt-2">
            {propData && Object.keys(propData).map((wydzial) => (
                <div onClick={() => {
                    propSetSelectedWydzial(wydzial);
                }} className="p-2 cursor-pointer hover:text-blue-700">{wydzial}</div>
            ))}
        </div>
    </div>)

}