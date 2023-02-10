import React, { useState, useRef } from "react";
import { camelCase, trim } from "lodash";
import api from "../utils/api";
import { Modal } from "../components/Modal";
import MarkdownInput from "../components/MarkdownInput";
import TextInputField from "../components/TextInput";
import IndigoButton from "../components/StyledButton";

export default function PublishArticle() {
  const [md, setMd] = useState("");
  const [articleData, setArticleData] = useState("");
  // as of react 18 all setState calls are batched
  const [showModal, setShowModal] = useState(false);
  const [notification, setNotification] = useState({
    title: undefined,
    msg: undefined,
    type: undefined,
  });

  const pubBtnRef = useRef(null);

  const handleChange = (e) => {
    setArticleData((data) => {
      return {
        ...data,
        [camelCase([e.target.name])]: trim(e.target.value),
      };
    });
  };

  const handlePublishClick = (e) => {
    e.stopPropagation();
    // disable button until api returns
    // should debounce? instead?
    if (pubBtnRef.current) {
      pubBtnRef.current.setAttribute("disabled", "disabled");
    }

    const payload = { ...articleData, markdown: md };
    api
      .createArticle(payload)
      .then(() => {
        setShowModal(true);
        setNotification({
          title: "Success",
          msg: "Article published successfully!",
          type: Modal.OK,
        });
      })
      .catch((err) => {
        setShowModal(true);
        setNotification({
          title: "Ooops",
          msg: err.message,
          type: Modal.ERROR,
        });
      })
      .finally(() => {
        pubBtnRef.current.removeAttribute("disabled");
      });
  };

  return (
    <>
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
      {/* Headless UI Dialog internally uses useEvent hook to optimize re-renders */}
      <Modal
        open={showModal}
        title={notification.title}
        msg={notification.msg}
        type={notification.type}
        setOpen={setShowModal}
      />
    </>
  );
}
