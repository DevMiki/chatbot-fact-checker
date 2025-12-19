import { useEffect, useMemo, useState } from "react";
import { cn, textStyles } from "../shared/ui";

const FUN_MESSAGES = [
  "invoking the holy spirits",
  "asking God if he knows something about it",
  "consulting the border collie council",
  "phoning a friend at the library",
  "bribing the LLM with binary treats",
  "praying that this works",
  "searching the universal sock drawer for answers",
  "asking the coffee machine for wisdom",
  "googling on a calculator",
  "shaking the magic 8-ball vigorously",
  "summoning the rubber duck for debugging therapy",
  "interrogating the error logs under a desk lamp",
  "spinning up the hamster wheel to power the servers",
  "consulting a crystal ball made of deprecated APIs",
  "translating ancient runes from the README",
  "sacrificing a semicolon to the syntax gods",
  "checking if Mercury is in retrograde (again)",
  "sending a carrier pigeon to the cloud",
];

const DOTS = [0, 1, 2];


function ThinkingIndicator({ active }) {
  const [messageIndex, setMessageIndex] = useState(0);
  const [messageOrder, setMessageOrder] = useState(FUN_MESSAGES);

  useEffect(() => {
    if (!active) {
      setMessageIndex(0);
      return;
    }
    const shuffled = [...FUN_MESSAGES].sort(() => Math.random() - 0.5);
    setMessageOrder(shuffled);
    setMessageIndex(0);
  }, [active]);

  useEffect(() => {
    if (!active) {
      setMessageIndex(0);
      return undefined;
    }

    const rotationMs = 2000;
    const timerId = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messageOrder.length);
    }, rotationMs);

    return () => clearInterval(timerId);
  }, [active, messageOrder.length]);

  const currentMessage = useMemo(
    () => messageOrder[messageIndex % messageOrder.length],
    [messageIndex, messageOrder]
  );

  if (!active) return null;

  return (
    <div
      className={cn(
        "flex items-center gap-4 rounded-2xl border-3 border-ink bg-white shadow-ink-sm px-4 py-3",
        "relative overflow-hidden"
      )}
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <div
        className={cn(
          "flex items-center gap-2 rounded-2xl border-2 border-ink bg-brand-purple text-white px-3 py-2 shadow-ink-sm"
        )}
      >
        <span className="font-semibold text-sm tracking-wide">Thinking</span>
        <span className="thinking-dots flex items-center gap-1" aria-hidden="true">
          {DOTS.map((dot) => (
            <span
              key={dot}
              className="block h-2 w-2 rounded-full bg-white"
              style={{ animationDelay: `${dot * 0.18}s` }}
            />
          ))}
        </span>
      </div>
      <div className={cn("text-base font-semibold text-ink", textStyles.subtext)}>
        {currentMessage}
      </div>
    </div>
  );
}

export default ThinkingIndicator;
