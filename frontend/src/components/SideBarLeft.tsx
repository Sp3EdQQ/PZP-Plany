import {useState} from "react"
import {Calendar} from "@/components/ui/calendar"
import {University} from "../../types/University.ts";

type SideBarLeftProps = {
    propData: University | null;
    propSetSelectedWydzial: (wydzial: string) => void;
};

export const SideBarLeft = ({propData, propSetSelectedWydzial}: SideBarLeftProps) => {
    const [date, setDate] = useState<Date | undefined>(new Date())

    return (<div className="w-1/5 flex-col p-6 bg-blue-700 h-screen">
        <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            className="rounded-md border w-64 bg-white "
        />
        <div className="pt-2">
            {propData && Object.keys(propData).map((wydzial) => (
                <div onClick={() => {
                    propSetSelectedWydzial(wydzial);
                }}
                     className="my-5 bg-white rounded-2xl *:m-5 p-2 cursor-pointer hover:bg-neutral-200">{wydzial}</div>
            ))}
        </div>
    </div>)

}