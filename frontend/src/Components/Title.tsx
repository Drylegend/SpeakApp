import { useState } from "react";
import axios from "axios";

type Props = {
  setMessages: any;
};

function Title({ setMessages }: Props) {
  const [isResetting, setIsResetting] = useState(false);

  // Reset the conversation
  const resetConversation = async () => {
    setIsResetting(true);

    await axios
      .get("http://localhost:8000/reset")
      .then((res) => {
        if (res.status === 200) {
          setMessages([]);
        } else {
          console.error("There was an error with the API request to the backend");
        }
      })
      .catch((err) => {
        console.error(err.messages);
      });

    setIsResetting(false);
  };

  return (
    <div className="relative w-full p-4 bg-gray-900 text-white font-bold shadow">
      {/* Reva University Logo */}
      <img
        src="/Reva logo new.png" // Reference the image in the public folder
        alt="Reva University Logo"
        className="absolute top-2 left-2 w-30 h-14" // Adjusted size for a small logo
      />

      {/* SpeakApp Title */}
      <div className="text-center text-lg italic">SpeakApp</div>

      {/* Reset Button */}
      <button
        onClick={resetConversation}
        className={
          "absolute top-2 right-2 transition-all duration-300 text-blue-300 hover:text-pink-500 " +
          (isResetting && "animate-pulse")
        }
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
          />
        </svg>
      </button>
    </div>
  );
}

export default Title;




























// import { useState } from "react";
// import axios from "axios";

// type Props = {
//   setMessages: any;
// };

// function Title({ setMessages }: Props) {
//   const [isResetting, setIsResetting] = useState(false);

//   // Reset the conversation
//   const resetConversation = async () => {
//     setIsResetting(true);

//     await axios
//       .get("http://localhost:8000/reset")
//       .then((res) => {
//         if (res.status == 200) {
            
//             setMessages([]);
//         } else {
//             console.error("There was an error with the api request to backend");
//         }
//       })
//       .catch((err) => {
//         console.error(err.messages);
//       });

//     setIsResetting(false);
//   };
//   return (
//     <div className="flex justify-between items-center w-full p-4 bg-gray-900 text-white font-bold shadow">
//       <div className="italic">SpeakApp</div>
//       <button onClick={resetConversation} className={"transition-all duration-300 text-blue-300 hover:text-pink-500 " +
//           (isResetting && "animate-pulse")}>
//         <svg
//           xmlns="http://www.w3.org/2000/svg"
//           fill="none"
//           viewBox="0 0 24 24"
//           strokeWidth={1.5}
//           stroke="currentColor"
//           className="size-6"
//         >
//           <path
//             strokeLinecap="round"
//             strokeLinejoin="round"
//             d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
//           />
//         </svg>
//       </button>
//     </div>
//   );
// }

// export default Title;
