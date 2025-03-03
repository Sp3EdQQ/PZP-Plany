import "./App.css";
import {SideBarLeft} from "@/components/SideBarLeft.tsx";
import {MainContent} from "@/components/MainContent.tsx";
import {useEffect, useState} from "react";
import {University} from "../types/University.ts";

function App() {
    const [data, setData] = useState<University | null>(null);
    const [selectedWydzial, setSelectedWydzial] = useState<string>();

    useEffect(() => {
        fetch("/plan.json")
            .then((res) => res.json())
            .then((json: University) => setData(json))
    }, []);
    return (
        <div className="bg-neutral-800 text-neutral-100 h-screen w-screen p-4">
            <div className="flex flex-row">
                <SideBarLeft propData={data} propSetSelectedWydzial={setSelectedWydzial}/>
                {data && (<MainContent propData={data} propSelectedWydzial={selectedWydzial || ""}/>)}
            </div>
        </div>
    );
}

export default App;

