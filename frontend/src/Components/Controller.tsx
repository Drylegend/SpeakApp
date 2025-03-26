import { useState, useEffect, useRef } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

const Controller = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  function createBlobURL(data: any) {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  }

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    const myMessage = { sender: "me", blobUrl };
    const messagesArr = [...messages, myMessage];

    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        await axios
          .post(`${import.meta.env.VITE_BACKEND_URL}/post-audio`, formData, {
            headers: {
              "Content-Type": "audio/mpeg",
            },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobURL(blob);

            const SpeakAiMessage = { sender: "SpeakApp", blobUrl: audio.src };
            messagesArr.push(SpeakAiMessage);
            setMessages(messagesArr);

            setIsLoading(false);
            audio.play();
          })
          .catch((err: any) => {
            console.error(err);
            setIsLoading(false);
          });
      });
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="relative flex flex-col w-full h-full bg-white">
      {/* Title */}
      <Title setMessages={setMessages} />

      {/* Fixed Background Image and Text */}
      <div className="fixed inset-0 flex flex-col justify-center items-center z-0 pointer-events-none">
        <div className="flex flex-col items-center ml-2"> {/* Slightly moved right */}
          <h1 className="text-3xl font-bold mb-4 text-gray-900">School of Computer Science</h1>
          <img
            src="/Club_Logo-removebg-preview.jpg"
            alt="Club Logo"
            className="w-60 h-60"
          />
        </div>
      </div>

      {/* Conversation and Recorder */}
      <div className="relative flex flex-col justify-between h-full overflow-y-scroll z-10">
        {/* Conversation */}
        <div className="mt-5 px-5">
          {messages?.map((audio, index) => (
            <div
              key={index + audio.sender}
              className={
                "flex flex-col " +
                (audio.sender === "SpeakApp" && "flex items-end")
              }
            >
              <div className="mt-4">
                <p
                  className={
                    audio.sender === "SpeakApp"
                      ? "text-right mr-2 italic text-green-500"
                      : "ml-2 italic text-blue-500"
                  }
                >
                  {audio.sender}
                </p>

                <audio
                  src={audio.blobUrl}
                  className="appearance-none"
                  controls
                />
              </div>
            </div>
          ))}

          {messages.length === 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send SpeakApp a message...
            </div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Gimme a few seconds...
            </div>
          )}

          {/* Auto-scroll anchor */}
          <div ref={messagesEndRef} />
        </div>

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div>
              <RecordMessage handleStop={handleStop} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controller;




























