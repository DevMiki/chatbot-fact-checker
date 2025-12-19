import { useEffect, useState } from "react";
import { send_chat_message as sendChatMessage } from "../features/chat/api";
import { healthCheck } from "../features/health/api";
import ChatInput from "../features/chat/components/ChatInput";
import ChatMessage from "../features/chat/components/ChatMessage";
import {
  branding,
  chips,
  cn,
  layout,
  pills,
  surfaces,
  textStyles,
} from "../shared/ui";
import ThinkingIndicator from "../components/ThinkingIndicator";

function App() {
  const [questionText, setQuestionText] = useState("");
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("Checking backend...");
  const [loading, setLoading] = useState(false);
  const [useLlm, setUseLlm] = useState(true);
  const [fileInputKey, setFileInputKey] = useState(0);

  useEffect(() => {
    healthCheck()
      .then(() => setStatus("Backend OK"))
      .catch(() => setStatus("Backend unavailable"));
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem("use_llm");
    if (stored !== null) {
      setUseLlm(stored !== "false" && stored !== "0");
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("use_llm", useLlm ? "true" : "false");
  }, [useLlm]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!questionText.trim()) return;

    setLoading(true);
    try {
      const message = await sendChatMessage(questionText, files, useLlm);
      appendNewMessage({
        question: questionText,
        answer: message.answer,
        referencedFiles: message.referenced_files,
        cacheHit: message.cache_hit,
      });
      resetForm();
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const appendNewMessage = (new_message) => {
    setMessages((previous_messages) => [
      { ...new_message, showFiles: false },
      ...previous_messages,
    ]);
  };

  const resetForm = () => {
    setQuestionText("");
    setFiles([]);
    setFileInputKey((prev) => prev + 1);
  };

  const toggleFiles = (index) => {
    setMessages((previous_messages) =>
      previous_messages.map((message, idx) =>
        idx === index ? { ...message, showFiles: !message.showFiles } : message
      )
    );
  };

  return (
    <div className={layout.page}>
      <div className={layout.container}>
        <header className={surfaces.shell}>
          <div className="flex items-center gap-4">
            <div className={branding.mark}>CF</div>
            <div>
              <div className="text-ink text-xl font-bold leading-tight">
                Chatbot Fact Checker
              </div>
              <div className={cn("mt-1", textStyles.subtext)}>
                Upload PDFs, ask questions, get quick references.
              </div>
            </div>
            <span
              className={cn(
                "ml-auto",
                pills.statusBase,
                status === "Backend OK" ? pills.statusOk : pills.statusWarn
              )}
            >
              {status}
            </span>
          </div>
          <div className="mt-4 space-y-1.5">
            <div className="flex flex-wrap gap-2">
              <span className={cn(chips.purple, "relative group")}>
                PDF uploads
                <span
                  className="pointer-events-none absolute bottom-[calc(100%+6px)] left-1/2 -translate-x-1/2 translate-y-1 whitespace-nowrap rounded-md bg-neutral-900 px-2 py-1 text-xs text-white opacity-0 shadow-sm transition duration-550 group-hover:translate-y-0 group-hover:opacity-100 group-focus-visible:translate-y-0 group-focus-visible:opacity-100"
                  aria-hidden
                >
                  informational only badge
                </span>
              </span>
              <span className={cn(chips.orange, "relative group")}>
                LLM Crazy Answers
                <span
                  className="pointer-events-none absolute bottom-[calc(100%+6px)] left-1/2 -translate-x-1/2 translate-y-1 whitespace-nowrap rounded-md bg-neutral-900 px-2 py-1 text-xs text-white opacity-0 shadow-sm transition duration-550 group-hover:translate-y-0 group-hover:opacity-100 group-focus-visible:translate-y-0 group-focus-visible:opacity-100"
                  aria-hidden
                >
                  informational only badge
                </span>
              </span>
              <span className={cn(chips.cyan, "relative group")}>
                Mock answers
                <span
                  className="pointer-events-none absolute bottom-[calc(100%+6px)] left-1/2 -translate-x-1/2 translate-y-1 whitespace-nowrap rounded-md bg-neutral-900 px-2 py-1 text-xs text-white opacity-0 shadow-sm transition duration-550 group-hover:translate-y-0 group-hover:opacity-100 group-focus-visible:translate-y-0 group-focus-visible:opacity-100"
                  aria-hidden
                >
                  informational only badge
                </span>
              </span>
              <span className={cn(chips.pink, "relative group")}>
                Fact-check files
                <span
                  className="pointer-events-none absolute bottom-[calc(100%+6px)] left-1/2 -translate-x-1/2 translate-y-1 whitespace-nowrap rounded-md bg-neutral-900 px-2 py-1 text-xs text-white opacity-0 shadow-sm transition duration-550 group-hover:translate-y-0 group-hover:opacity-100 group-focus-visible:translate-y-0 group-focus-visible:opacity-100"
                  aria-hidden
                >
                  informational only badge
                </span>
              </span>
              <span className={cn(chips.gold, "relative group")}>
                Cache & Redis fallback
                <span
                  className="pointer-events-none absolute bottom-[calc(100%+6px)] left-1/2 -translate-x-1/2 translate-y-1 whitespace-nowrap rounded-md bg-neutral-900 px-2 py-1 text-xs text-white opacity-0 shadow-sm transition duration-550 group-hover:translate-y-0 group-hover:opacity-100 group-focus-visible:translate-y-0 group-focus-visible:opacity-100"
                  aria-hidden
                >
                  informational only badge
                </span>
              </span>
            </div>
          </div>
        </header>

        <section className={surfaces.panel}>
          <ChatInput
            question={questionText}
            files={files}
            useLlm={useLlm}
            onQuestionChange={setQuestionText}
            onFilesChange={setFiles}
            onUseLlmChange={setUseLlm}
            onSubmit={handleSubmit}
            loading={loading}
            fileInputKey={fileInputKey}
          />
        </section>

        <ThinkingIndicator active={loading} />

        <section className={layout.stack}>
          {messages.length === 0 && (
            <div className={surfaces.muted}>
              No messages yet. Ask a question!
            </div>
          )}
          {messages.map((message, idx) => (
            <ChatMessage
              key={`${message.question}-${idx}`}
              message={message}
              onToggleFiles={() => toggleFiles(idx)}
            />
          ))}
        </section>
      </div>
    </div>
  );
}

export default App;
