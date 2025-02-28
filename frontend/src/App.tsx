import "./App.css"
import { CalendarDiv } from "@/components/CalendarDiv.tsx"
import { Header } from "@/components/Header.tsx"

function App() {

  return <div className="bg-neutral-800 text-neutral-100 h-screen w-screen">
    <div className="flex flex-row">
      <CalendarDiv />
      <Header />
    </div>
  </div>
}

export default App
