import "./App.css";
import {SideBarLeft} from "@/components/SideBarLeft.tsx";
import {MainContent} from "@/components/MainContent.tsx";
import {useEffect, useState} from "react";
import {University} from "../types/University.ts";

function App() {
    const [data, setData] = useState<University | null>(null);
    const [selectedWydzial, setSelectedWydzial] = useState<string>("");

    useEffect(() => {
        fetch("/plan.json")
            .then((res) => res.json())
            .then((json: University) => setData(json))
            .catch((error) => console.error("Error fetching plan.json:", error));
    }, []);

    const handleRefresh = () => {
        window.location.reload();
    };

    return (
        <div className="w-screen overflow-x-hidden">
            <div
                className="fixed top-0 left-0 w-full bg-custom-blue text-white flex p-2 z-20 "

            >
                <div className="cursor-pointer" onClick={() => {
                    handleRefresh()
                }}>
                    <div className="flex items-center">
                        <img
                            src="/logo.png"
                            alt="logo"
                            className="h-15"
                        />
                        <img
                            src="/topwrite.png"
                            alt="topwrite"
                            className="h-15"
                        />
                    </div>
                </div>

            </div>
            <div className="flex flex-row bg-custom-blue min-h-screen pt-16">
                <SideBarLeft propData={data} propSetSelectedWydzial={setSelectedWydzial}/>
                {data && <MainContent propData={data} propSelectedWydzial={selectedWydzial}/>}
            </div>
        </div>
    );
}

export default App;