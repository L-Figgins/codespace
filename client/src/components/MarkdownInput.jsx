import React, from "react";
import ReactMarkdown from "react-markdown";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import js from "react-syntax-highlighter/dist/esm/languages/hljs/javascript";
import python from "react-syntax-highlighter/dist/esm/languages/hljs/javascript";
import { dark } from "react-syntax-highlighter/dist/esm/styles/hljs";
import Tabs from "./Tabs";

SyntaxHighlighter.registerLanguage("javascript", js);
SyntaxHighlighter.registerLanguage("python", python);

const tabs = ["Write", "Preview"];

/**
 *
 * @param {Object} obj
 * @param {String} obj.md - markdown
 */
function MarkdownInput({ md, handleChange }) {
  return (
    <div>
      <Tabs tabs={tabs}>
        <div className="xl:w-full">
          <textarea
            onChange={handleChange}
            className="
                    form-control
                    block
                    w-full
                    px-3
                    py-1.5
                    text-base
                    font-normal
                    text-gray-700
                    bg-white bg-clip-padding
                    border border-solid border-gray-300
                    rounded
                    transition
                    ease-in-out
                    m-0
                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
                "
            id="exampleFormControlTextarea1"
            rows="3"
            placeholder="Your message"
            value={md}
          ></textarea>
        </div>

        <ReactMarkdown
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              return !inline && match ? (
                <SyntaxHighlighter
                  children={String(children).replace(/\n$/, "")}
                  style={dark}
                  language={match[1]}
                  PreTag="div"
                  {...props}
                />
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {md}
        </ReactMarkdown>
      </Tabs>
    </div>
  );
}
export default MarkdownInput;
