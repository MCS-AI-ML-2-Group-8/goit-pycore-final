import { Chat } from "./components/Chat/Chat";
import "./App.css";

function App() {
  const [count, setCount] = useState(0)

  // Use this snippet to verify CORS settings in localhost

  // const fetchContacts = async() => {
  //   const response = await fetch("http://localhost:8000/contacts");
  //   const contacts = await response.json()
  //   console.info(contacts)
  // }

  // useEffect(() => { fetchContacts() }, [])

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <Chat />
    </div>
  );
}

export default App;
