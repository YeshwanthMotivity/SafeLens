// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import "./App.css";

// // Utility to format Gemini Output
// const formatLlmOutput = (text) => {
//   if (!text) return null;
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // Reusable Response Card
// const ResponseCard = ({ title, icon, content, colorClass }) => (
//   <div className={`card ${colorClass}`}>
//     <h3 className="card-title">
//       <span className="mr-2">{icon}</span> {title}
//     </h3>
//     <div className="card-content">
//       {title === "Gemini Output" ? formatLlmOutput(content) : content}
//     </div>
//   </div>
// );

// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post(
//         "http://127.0.0.1:8001/api/v1/text/analyze",
//         { text: userInput }
//       );
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   const cardData = response
//     ? [
//       { title: "Original Input", icon: "📝", content: response.original_text, colorClass: "border-indigo" },
//       { title: "Masked Text", icon: "🧱", content: response.masked_text, colorClass: "border-orange" },
//       { title: "Selected Technique", icon: "🎯", content: response.selected_prompt_technique, colorClass: "border-violet" },
//       { title: "Prompt Template", icon: "🛠️", content: response.prompt_template, colorClass: "border-teal" }, // NEW
//       { title: "Optimized Prompt (Groq)", icon: "⚡", content: response.optimized_prompt, colorClass: "border-yellow" }, // Original Optimizer output
//       { title: "Gemini Output", icon: "🤖", content: response.llm_response, colorClass: "border-emerald" },
//     ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <ResponseCard key={idx} {...card} />
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import "./App.css";

// // Utility to format Gemini Output
// const formatLlmOutput = (text) => {
//   if (!text) return null;
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // Reusable Response Card
// const ResponseCard = ({ title, icon, content, colorClass }) => (
//   <div className={`card ${colorClass}`}>
//     <h3 className="card-title">
//       <span className="mr-2">{icon}</span> {title}
//     </h3>
//     <div className="card-content">
//       {title === "Gemini Output" ? formatLlmOutput(content) : content}
//     </div>
//   </div>
// );

// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post(
//         "http://127.0.0.1:8001/api/v1/text/analyze",
//         { text: userInput }
//       );
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   const cardData = response
//     ? [
//         // ROW 1: 3 equal columns (Original Input, Masked Text, Selected Technique)
//         { title: "Original Input", icon: "📝", content: response.original_text, colorClass: "border-indigo", layoutClass: "card-span-1" },
//         { title: "Masked Text", icon: "🧱", content: response.masked_text, colorClass: "border-orange", layoutClass: "card-span-1" },
//         { title: "Selected Technique", icon: "🎯", content: response.selected_prompt_technique, colorClass: "border-violet", layoutClass: "card-span-1" },

//         // ROW 2: Full width (Optimized Prompt)
//         { title: "Optimized Prompt (Groq)", icon: "⚡", content: response.optimized_prompt, colorClass: "border-yellow", layoutClass: "card-span-3" },

//         // ROW 3: Full width (Prompt Template)
//         { title: "Prompt Template", icon: "🛠️", content: response.prompt_template, colorClass: "border-teal", layoutClass: "card-span-3" },
        
//         // ROW 4: Full width (Gemini Output)
//         { title: "Gemini Output", icon: "🤖", content: response.llm_response, colorClass: "border-emerald", layoutClass: "card-span-3" },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             // New wrapping div uses the layoutClass to control grid span
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import "./App.css";

// /* ===== Utility: Format Gemini Output ===== */
// const formatLlmOutput = (text) => {
//   if (!text) return null;
//   // Split by **text** to apply bold styling dynamically
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// /* ===== Reusable Response Card Component ===== */
// const ResponseCard = ({ title, icon, content, colorClass, toggleContent }) => {
//   const [showReasoning, setShowReasoning] = useState(false);

//   return (
//     <div className={`card ${colorClass}`}>
//       <div className="flex justify-between items-start">
//         <h3 className="card-title">
//           <span className="mr-2">{icon}</span> {title}
//         </h3>

//         {/* Show toggle button only if reasoning exists */}
//         {toggleContent && (
//           <button
//             className="toggle-button"
//             onClick={() => setShowReasoning(!showReasoning)}
//           >
//             {showReasoning ? "Hide Reasoning" : "Show Reasoning"}
//           </button>
//         )}
//       </div>

//       <div className="card-content">
//         {content}

//         {/* Conditionally render reasoning */}
//         {showReasoning && toggleContent && (
//           <div className="reasoning-content">
//             <p className="highlight-bold mb-2">Reasoning:</p>
//             {toggleContent}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// /* ===== Main Application Component ===== */
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   /* ===== Handle Submit ===== */
//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post(
//         "http://127.0.0.1:8001/api/v1/text/analyze",
//         { text: userInput }
//       );
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   /* ===== Prepare Data for Cards ===== */
//   const cardData = response
//     ? [
//         // Row 1: Original Input | Masked Text | Technique
//         {
//           title: "Original Input",
//           icon: "📝",
//           content: response.original_text,
//           colorClass: "border-indigo",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Masked Text",
//           icon: "🧱",
//           content: response.masked_text,
//           colorClass: "border-orange",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Selected Technique",
//           icon: "🎯",
//           content: response.selected_prompt_technique,
//           colorClass: "border-violet",
//           layoutClass: "card-span-1",
//         },

//         // Row 2: Optimized Prompt
//         {
//           title: "Optimized Prompt",
//           icon: "⚡",
//           content: response.optimized_prompt,
//           colorClass: "border-yellow",
//           layoutClass: "card-span-3",
//         },

//         // Row 3: Prompt Template + Reasoning
//         {
//           title: "Prompt Template (Groq)",
//           icon: "🛠️",
//           content: response.prompt_template,
//           colorClass: "border-teal",
//           layoutClass: "card-span-3",
//           toggleContent: response.prompt_reasoning,
//         },

//         // Row 4: Gemini Output (formatted)
//         {
//           title: "Gemini Output",
//           icon: "🤖",
//           content: formatLlmOutput(response.llm_response),
//           colorClass: "border-emerald",
//           layoutClass: "card-span-3",
//         },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       {/* ===== Header Section ===== */}
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       {/* ===== Input Section ===== */}
//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {/* ===== Feedback States ===== */}
//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {/* ===== Response Section ===== */}
//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import ReactMarkdown from "react-markdown";
// import "./App.css";

// /* ===== Utility: Format Gemini Output ===== */
// const formatLlmOutput = (text) => {
//   if (!text) return null;
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// /* ===== Reusable Response Card Component ===== */
// const ResponseCard = ({ title, icon, content, colorClass, toggleContent, isFormatted }) => {
//   const [showReasoning, setShowReasoning] = useState(false);

//   return (
//     <div className={`card ${colorClass}`}>
//       <div className="flex justify-between items-start">
//         <h3 className="card-title">
//           <span className="mr-2">{icon}</span> {title}
//         </h3>

//         {/* Show toggle button only if reasoning exists */}
//         {toggleContent && (
//           <button
//             className="toggle-button"
//             onClick={() => setShowReasoning(!showReasoning)}
//           >
//             {showReasoning ? "Hide Reasoning" : "Show Reasoning"}
//           </button>
//         )}
//       </div>

//       <div className="card-content">
//         {/* Use markdown only for string content */}
//         {isFormatted ? (
//           content
//         ) : (
//           <ReactMarkdown>{content || ""}</ReactMarkdown>
//         )}

//         {/* Conditionally render reasoning only when toggled */}
//         {showReasoning && toggleContent && (
//           <div className="reasoning-content mt-2">
//             <p className="highlight-bold mb-2">Reasoning:</p>
//             <ReactMarkdown>{toggleContent}</ReactMarkdown>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// /* ===== Main Application Component ===== */
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   /* ===== Handle Submit ===== */
//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post(
//         "http://127.0.0.1:8001/api/v1/text/analyze",
//         { text: userInput }
//       );
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   /* ===== Prepare Data for Cards ===== */
//   const cardData = response
//     ? [
//         // Row 1: Original Input | Masked Text | Technique
//         {
//           title: "Original Input",
//           icon: "📝",
//           content: response.original_text,
//           colorClass: "border-indigo",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Masked Text",
//           icon: "🧱",
//           content: response.masked_text,
//           colorClass: "border-orange",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Selected Technique",
//           icon: "🎯",
//           content: response.selected_prompt_technique,
//           colorClass: "border-violet",
//           layoutClass: "card-span-1",
//         },

//         // Row 2: Optimized Prompt
//         {
//           title: "Optimized Prompt",
//           icon: "⚡",
//           content: response.optimized_prompt,
//           colorClass: "border-yellow",
//           layoutClass: "card-span-3",
//         },

//         // Row 3: Prompt Template + Reasoning toggle
//         {
//           title: "Prompt Template (Groq)",
//           icon: "🛠️",
//           content: response.prompt_template,
//           colorClass: "border-teal",
//           layoutClass: "card-span-3",
//           toggleContent: response.prompt_reasoning,
//         },

//         // Row 4: Gemini Output (formatted manually)
//         {
//           title: "Gemini Output",
//           icon: "🤖",
//           content: formatLlmOutput(response.llm_response),
//           colorClass: "border-emerald",
//           layoutClass: "card-span-3",
//           isFormatted: true, // tells the component not to markdown this
//         },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       {/* ===== Header Section ===== */}
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       {/* ===== Input Section ===== */}
//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {/* ===== Feedback States ===== */}
//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {/* ===== Response Section ===== */}
//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import ReactMarkdown from "react-markdown";
// import "./App.css";

// // ===== Utility: Format Gemini Output =====
// const formatLlmOutput = (text) => {
//   if (!text) return "";
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // ===== Response Card Component =====
// const ResponseCard = ({ title, icon, content, colorClass, toggleContent, isFormatted }) => {
//   const [showReasoning, setShowReasoning] = useState(false);

//   return (
//     <div className={`card ${colorClass}`}>
//       <div className="flex justify-between items-start">
//         <h3 className="card-title">
//           <span className="mr-2">{icon}</span> {title}
//         </h3>
// {/* 
//         {toggleContent && toggleContent.trim() !== "" && (
//           <button
//             className="toggle-button"
//             onClick={() => setShowReasoning((prev) => !prev)}
//           >
//             {showReasoning ? "Hide Reasoning" : "Show Reasoning"}
//           </button>
//         )} */}
//       </div>

//       <div className="card-content">
//         {isFormatted ? content : <ReactMarkdown>{content || ""}</ReactMarkdown>}

//         {showReasoning && toggleContent && (
//           <div className="reasoning-content mt-2">
//             <p className="highlight-bold mb-2">Reasoning:</p>
//             <ReactMarkdown>{toggleContent}</ReactMarkdown>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// // ===== Main App =====
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post("http://127.0.0.1:8001/api/v1/text/analyze", {
//         text: userInput,
//       });
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   const cardData = response
//     ? [
//         {
//           title: "Original Input",
//           icon: "📝",
//           content: response.original_text,
//           colorClass: "border-indigo",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Masked Text",
//           icon: "🧱",
//           content: response.masked_text,
//           colorClass: "border-orange",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Selected Technique",
//           icon: "🎯",
//           content: response.selected_prompt_technique,
//           colorClass: "border-violet",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Optimized Prompt",
//           icon: "⚡",
//           content: response.optimized_prompt,
//           colorClass: "border-yellow",
//           layoutClass: "card-span-3",
//         },
//         {
//           title: "Prompt Template (Groq)",
//           icon: "🛠️",
//           content: response.prompt_template,
//           colorClass: "border-teal",
//           layoutClass: "card-span-3",
//           toggleContent: response.prompt_reasoning || "No reasoning section detected.",
//         },
//         {
//           title: "Gemini Output",
//           icon: "🤖",
//           content: formatLlmOutput(response.llm_response),
//           colorClass: "border-emerald",
//           layoutClass: "card-span-3",
//           isFormatted: true,
//         },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import ReactMarkdown from "react-markdown";
// import "./App.css";

// // ===== Utility: Format Gemini Output =====
// const formatLlmOutput = (text) => {
//   if (!text) return "";
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // ===== Response Card Component =====
// const ResponseCard = ({ title, icon, content, colorClass, isFormatted }) => (
//   <div className={`card ${colorClass}`}>
//     <h3 className="card-title">
//       <span className="mr-2">{icon}</span> {title}
//     </h3>
//     <div className="card-content">
//       {isFormatted ? content : <ReactMarkdown>{content || ""}</ReactMarkdown>}
//     </div>
//   </div>
// );

// // ===== Main App =====
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post("http://127.0.0.1:8001/api/v1/text/analyze", {
//         text: userInput,
//       });
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   const cardData = response
//     ? [
//         { title: "Original Input", icon: "📝", content: response.original_text, colorClass: "border-indigo" },
//         { title: "Masked Text", icon: "🧱", content: response.masked_text, colorClass: "border-orange" },
//         { title: "Selected Technique", icon: "🎯", content: response.selected_prompt_technique, colorClass: "border-violet" },
//         { title: "Optimized Prompt", icon: "⚡", content: response.optimized_prompt, colorClass: "border-yellow" },
//         { title: "Refined Prompt (Groq)", icon: "🛠️", content: response.prompt_template, colorClass: "border-teal" },
//         { title: "Gemini Output", icon: "🤖", content: formatLlmOutput(response.llm_response), colorClass: "border-emerald", isFormatted: true },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <ResponseCard key={idx} {...card} />
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback } from "react";
// import axios from "axios";
// import ReactMarkdown from "react-markdown";
// import "./App.css";

// // ===== Utility: Format Gemini Output =====
// const formatLlmOutput = (text) => {
//   if (!text) return "";
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // ===== Response Card Component =====
// const ResponseCard = ({ title, icon, content, colorClass, isFormatted }) => {
//   return (
//     <div className={`card ${colorClass}`}>
//       <div className="flex justify-between items-start">
//         <h3 className="card-title">
//           <span className="mr-2">{icon}</span> {title}
//         </h3>
//       </div>

//       <div className="card-content">
//         {isFormatted ? content : <ReactMarkdown>{content || ""}</ReactMarkdown>}
//       </div>
//     </div>
//   );
// };

// // ===== Main App =====
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim()) return;
//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     try {
//       const res = await axios.post("http://127.0.0.1:8001/api/v1/text/analyze", {
//         text: userInput,
//       });
//       setResponse(res.data);
//     } catch (err) {
//       console.error(err);
//       setError("❌ Could not connect to backend.");
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput]);

//   const cardData = response
//     ? [
//         {
//           title: "Original Input",
//           icon: "📝",
//           content: response.original_text,
//           colorClass: "border-indigo",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Masked Text",
//           icon: "🧱",
//           content: response.masked_text,
//           colorClass: "border-orange",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Selected Technique",
//           icon: "🎯",
//           content: response.selected_prompt_technique,
//           colorClass: "border-violet",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Optimized Prompt",
//           icon: "⚡",
//           content: response.optimized_prompt,
//           colorClass: "border-yellow",
//           layoutClass: "card-span-3",
//         },
//         {
//           title: "Prompt Template (Groq)",
//           icon: "🛠️",
//           content: response.prompt_template,
//           colorClass: "border-teal",
//           layoutClass: "card-span-3",
//         },
//         {
//           title: "Gemini Output",
//           icon: "🤖",
//           content: formatLlmOutput(response.llm_response),
//           colorClass: "border-emerald",
//           layoutClass: "card-span-3",
//           isFormatted: true,
//         },
//       ]
//     : [];

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         <textarea
//           placeholder="Type your prompt here..."
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Processing..." : "Analyze & Generate"}
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

// import React, { useState, useCallback, useRef } from "react"; // 1. Added useRef
// import axios from "axios";
// import ReactMarkdown from "react-markdown";
// import "./App.css";

// // ===== Utility: Format Gemini Output (kept the same) =====
// const formatLlmOutput = (text) => {
//   if (!text) return "";
//   const parts = text.split(/(\*\*.*?\*\*)/g);
//   return parts.map((part, index) => {
//     if (part.startsWith("**") && part.endsWith("**")) {
//       return (
//         <strong key={index} className="highlight-bold">
//           {part.slice(2, -2)}
//         </strong>
//       );
//     }
//     return <span key={index}>{part}</span>;
//   });
// };

// // ===== Response Card Component (kept the same) =====
// const ResponseCard = ({ title, icon, content, colorClass, isFormatted }) => {
//   return (
//     <div className={`card ${colorClass}`}>
//       <div className="flex justify-between items-start">
//         <h3 className="card-title">
//           <span className="mr-2">{icon}</span> {title}
//         </h3>
//       </div>

//       <div className="card-content">
//         {isFormatted ? content : <ReactMarkdown>{content || ""}</ReactMarkdown>}
//       </div>
//     </div>
//   );
// };

// // ===== Main App =====
// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [imageFile, setImageFile] = useState(null); // 2. New state for image file
//   const [response, setResponse] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const fileInputRef = useRef(null); // 3. Ref for hidden file input

//   // Function to trigger the hidden file input
//   const handleImageUploadClick = () => {
//     fileInputRef.current.click();
//   };

//   // Function to handle file selection
//   const handleFileChange = (event) => {
//     const file = event.target.files[0];
//     if (file) {
//       setImageFile(file);
//       // Optional: Clear text input when image is selected
//       // setUserInput("");
//     }
//   };
  
//   // 4. Combined handleSubmit for text and image
//   const handleSubmit = useCallback(async () => {
//     if (!userInput.trim() && !imageFile) return;

//     setLoading(true);
//     setResponse(null);
//     setError(null);

//     const isImageSubmission = !!imageFile;
//     const endpoint = isImageSubmission
//       ? "http://127.0.0.1:8001/api/v1/image/analyze_image"
//       : "http://127.0.0.1:8001/api/v1/text/analyze";
    
//     try {
//       let res;
//       if (isImageSubmission) {
//         // Handle image upload
//         const formData = new FormData();
//         formData.append("file", imageFile); // 'file' matches the backend endpoint argument
        
//         res = await axios.post(endpoint, formData, {
//           headers: {
//             "Content-Type": "multipart/form-data",
//           },
//         });
        
//         // After successful upload, clear the image state and input value
//         setImageFile(null);
//         if (fileInputRef.current) fileInputRef.current.value = ""; 

//       } else {
//         // Handle text input (original logic)
//         res = await axios.post(endpoint, { text: userInput });
//         setUserInput(""); // Clear text input after successful submission
//       }

//       setResponse(res.data);
//     } catch (err) {
//       console.error(err.response ? err.response.data : err);
//       setError(`❌ Could not process ${isImageSubmission ? 'image' : 'text'}. Check console for details.`);
//     } finally {
//       setLoading(false);
//     }
//   }, [userInput, imageFile]); // Added imageFile to dependencies

//   const cardData = response
//     ? [
//         {
//           title: response.original_text.length > 50 ? "Original Input (OCR)" : "Original Input", // Update title for clarity
//           icon: response.original_text.length > 50 ? "📄" : "📝",
//           content: response.original_text,
//           colorClass: "border-indigo",
//           layoutClass: "card-span-1",
//         },
//         // ... rest of cardData remains the same
//         {
//           title: "Masked Text",
//           icon: "🧱",
//           content: response.masked_text,
//           colorClass: "border-orange",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Selected Technique",
//           icon: "🎯",
//           content: response.selected_prompt_technique,
//           colorClass: "border-violet",
//           layoutClass: "card-span-1",
//         },
//         {
//           title: "Optimized Prompt",
//           icon: "⚡",
//           content: response.optimized_prompt,
//           colorClass: "border-yellow",
//           layoutClass: "card-span-3",
//         },
//         {
//           title: "Prompt Template (Groq)",
//           icon: "🛠️",
//           content: response.prompt_template,
//           colorClass: "border-teal",
//           layoutClass: "card-span-3",
//         },
//         {
//           title: "Gemini Output",
//           icon: "🤖",
//           content: formatLlmOutput(response.llm_response),
//           colorClass: "border-emerald",
//           layoutClass: "card-span-3",
//           isFormatted: true,
//         },
//       ]
//     : [];

//   // Determine the current placeholder/message
//   const inputPlaceholder = imageFile
//     ? `Image selected: ${imageFile.name}. Click Analyze & Generate to process.`
//     : "Type your prompt here...";

//   return (
//     <div className="app-upgraded">
//       <header className="app-header">
//         <h1>🔐 Prompt Assistant AI</h1>
//         <p>Real-time prompt analysis & LLM response generation</p>
//       </header>

//       <div className="input-section">
//         {/* New input container for styling the text area and buttons */}
//         <div className="input-container">
//           {/* Hidden file input */}
//           <input
//             type="file"
//             ref={fileInputRef}
//             onChange={handleFileChange}
//             accept="image/*"
//             style={{ display: "none" }}
//           />

//           {/* New "+" button for image upload */}
//           <button
//             className="upload-button"
//             onClick={handleImageUploadClick}
//             disabled={loading}
//             title="Upload Image (OCR)"
//           >
//             +
//           </button>
          
//           <textarea
//             placeholder={inputPlaceholder}
//             value={imageFile ? "" : userInput} // Clear text if image is selected
//             onChange={(e) => setUserInput(e.target.value)}
//             disabled={loading || !!imageFile} // Disable if loading or image is selected
//           />
//         </div>
        
//         {imageFile && (
//             <p className="image-info">
//                 🖼️ **Image Selected:** {imageFile.name} 
//                 <span className="remove-image" onClick={() => {
//                     setImageFile(null);
//                     if (fileInputRef.current) fileInputRef.current.value = "";
//                 }}> (Remove)</span>
//             </p>
//         )}

//         <button onClick={handleSubmit} disabled={loading || (!userInput.trim() && !imageFile)}>
//           {loading 
//             ? "Processing..." 
//             : imageFile 
//               ? "Analyze Image & Generate"
//               : "Analyze & Generate"
//           }
//         </button>
//       </div>

//       {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
//       {error && <div className="error-card">{error}</div>}

//       {response && (
//         <div className="response-section">
//           {cardData.map((card, idx) => (
//             <div key={idx} className={card.layoutClass}>
//               <ResponseCard {...card} />
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import React, { useState, useCallback, useRef } from "react"; // 1. Added useRef
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

// ===== Utility: Format Gemini Output (kept the same) =====
const formatLlmOutput = (text) => {
  if (!text) return "";
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={index} className="highlight-bold">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return <span key={index}>{part}</span>;
  });
};

// ===== Response Card Component (kept the same) =====
const ResponseCard = ({ title, icon, content, colorClass, isFormatted }) => {
  return (
    <div className={`card ${colorClass}`}>
      <div className="flex justify-between items-start">
        <h3 className="card-title">
          <span className="mr-2">{icon}</span> {title}
        </h3>
      </div>

      <div className="card-content">
        {isFormatted ? content : <ReactMarkdown>{content || ""}</ReactMarkdown>}
      </div>
    </div>
  );
};

// ===== Main App =====
function App() {
  const [userInput, setUserInput] = useState("");
  const [imageFile, setImageFile] = useState(null); // 2. New state for image file
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null); // 3. Ref for hidden file input

  // Function to trigger the hidden file input
  const handleImageUploadClick = () => {
    fileInputRef.current.click();
  };

  // Function to handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file);
      // Optional: Clear text input when image is selected
      // setUserInput("");
    }
  };
  
  // 4. Combined handleSubmit for text and image
  const handleSubmit = useCallback(async () => {
    if (!userInput.trim() && !imageFile) return;

    setLoading(true);
    setResponse(null);
    setError(null);

    const isImageSubmission = !!imageFile;
    const endpoint = isImageSubmission
      ? "http://127.0.0.1:8000/api/v1/image/analyze_image"
      : "http://127.0.0.1:8000/api/v1/text/analyze";
    
    try {
      let res;
      if (isImageSubmission) {
        // Handle image upload
        const formData = new FormData();
        formData.append("file", imageFile); // 'file' matches the backend endpoint argument
        
        res = await axios.post(endpoint, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        
        // After successful upload, clear the image state and input value
        setImageFile(null);
        if (fileInputRef.current) fileInputRef.current.value = ""; 

      } else {
        // Handle text input (original logic)
        res = await axios.post(endpoint, { text: userInput });
        setUserInput(""); // Clear text input after successful submission
      }

      setResponse(res.data);
    } catch (err) {
      console.error(err.response ? err.response.data : err);
      setError(`❌ Could not process ${isImageSubmission ? 'image' : 'text'}. Check console for details.`);
    } finally {
      setLoading(false);
    }
  }, [userInput, imageFile]); // Added imageFile to dependencies

  const cardData = response
    ? [
        {
          title: response.original_text.length > 50 ? "Original Input (OCR)" : "Original Input", // Update title for clarity
          icon: response.original_text.length > 50 ? "📄" : "📝",
          content: response.original_text,
          colorClass: "border-indigo",
          layoutClass: "card-span-1",
        },
        // ... rest of cardData remains the same
        {
          title: "Masked Text",
          icon: "🧱",
          content: response.masked_text,
          colorClass: "border-orange",
          layoutClass: "card-span-1",
        },
        {
          title: "Selected Technique",
          icon: "🎯",
          content: response.selected_prompt_technique,
          colorClass: "border-violet",
          layoutClass: "card-span-1",
        },
        {
          title: "Optimized Prompt",
          icon: "⚡",
          content: response.optimized_prompt,
          colorClass: "border-yellow",
          layoutClass: "card-span-3",
        },
        {
          title: "Prompt Template (Groq)",
          icon: "🛠️",
          content: response.prompt_template,
          colorClass: "border-teal",
          layoutClass: "card-span-3",
        },
        {
          title: "Gemini Output",
          icon: "🤖",
          content: formatLlmOutput(response.llm_response),
          colorClass: "border-emerald",
          layoutClass: "card-span-3",
          isFormatted: true,
        },
      ]
    : [];

  // Determine the current placeholder/message
  const inputPlaceholder = imageFile
    ? `Image selected: ${imageFile.name}. Click Analyze & Generate to process.`
    : "Type your prompt here...";

  return (
    <div className="app-upgraded">
      <header className="app-header">
        <h1>🔐 Prompt Assistant AI</h1>
        <p>Real-time prompt analysis & LLM response generation</p>
      </header>

      <div className="input-section">
        {/* New input container for styling the text area and buttons */}
        <div className="input-container">
          {/* Hidden file input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            style={{ display: "none" }}
          />
          
          {/* 1. Moved "+" button to the left side in the JSX */}
          <button
            className="upload-button"
            onClick={handleImageUploadClick}
            disabled={loading}
            title="Upload Image (OCR)"
          >
            +
          </button>
          
          <textarea
            placeholder={inputPlaceholder}
            value={imageFile ? "" : userInput} // Clear text if image is selected
            onChange={(e) => setUserInput(e.target.value)}
            disabled={loading || !!imageFile} // Disable if loading or image is selected
            className={imageFile ? 'image-selected' : ''} // Add class for padding adjustment
          />
        </div>
        
        {imageFile && (
            <p className="image-info">
                🖼️ **Image Selected:** {imageFile.name} 
                <span className="remove-image" onClick={() => {
                    setImageFile(null);
                    if (fileInputRef.current) fileInputRef.current.value = "";
                }}> (Remove)</span>
            </p>
        )}

        <button onClick={handleSubmit} disabled={loading || (!userInput.trim() && !imageFile)}>
          {loading 
            ? "Processing..." 
            : imageFile 
              ? "Analyze Image & Generate"
              : "Analyze & Generate"
          }
        </button>
      </div>

      {loading && <div className="loader">⏳ Analyzing and Generating...</div>}
      {error && <div className="error-card">{error}</div>}

      {response && (
        <div className="response-section">
          {cardData.map((card, idx) => (
            <div key={idx} className={card.layoutClass}>
              <ResponseCard {...card} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
