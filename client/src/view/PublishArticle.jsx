import React, { useState, useRef } from "react";
import MarkdownInput from "../components/MarkdownInput";
import TextInputField from "../components/TextInput";
import IndigoButton from "../components/StyledButton";
import { camelCase, trim } from "lodash";
import api from "../api/api";

export default function PublishArticle() {
  const [md, setMd] = useState("");
  const [articleData, setArticleData] = useState("");
  const pubBtnRef = useRef(null);

  const handleChange = (e) => {
    setArticleData((data) => {
      return {
        ...data,
        // [e.target.name]: e.target.value,
        [camelCase([e.target.name])]: trim(e.target.value),
      };
    });
  };

  const handlePublishClick = (e) => {
    e.stopPropagation();
    //disable button until api returns
    if (pubBtnRef.current) {
      pubBtnRef.current.setAttribute("disabled", "disabled");
    }

    const payload = { ...articleData, markdown: md };
    api
      .createArticle(payload)
      .then((res) => console.log(res))
      .catch((err) => console.error(err))
      .finally(() => {
        pubBtnRef.current.removeAttribute("disabled");
      });
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="flex justify-center text-lg">Publish Article</h1>
      <TextInputField
        title="title"
        id="title"
        placeholder="Article Title"
        handleChange={handleChange}
      />
      <TextInputField
        title="description"
        id="description"
        placeholder="Article Description"
        handleChange={handleChange}
      />
      <MarkdownInput
        md={md}
        handleChange={(e) => {
          e.stopPropagation();
          setMd(e.target.value);
        }}
      />
      <IndigoButton
        ref={pubBtnRef}
        id="publish"
        text="Publish"
        handleClick={handlePublishClick}
      />
    </div>
  );
}
