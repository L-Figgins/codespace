import ReactMarkdown from "react-markdown";
import react, { useState } from "react";
import api from "../api/api";

export default function CreateArticle() {
  const [md, setMd] = useState(`\`\`\`def code():\`\`\``);
  const [showPreview, setShowPreview] = useState(false);
  const [articleData, setArticleData] = useState({});

  const handleChange = (e) => {
    setArticleData((data) => {
      return {
        ...data,
        [e.target.name]: e.target.value,
        // [camelCase([e.target.name])]: trim(e.target.value),
      };
    });
  };

  function onPreviewClick(e) {
    setShowPreview((show) => {
      return !show;
    });
  }

  function onSaveClick() {
    console.log(articleData);
    api.createArticle(articleData);
  }

  console.log(md);

  return (
    <div>
      <h1>markdown generator</h1>
      <div>
        <div class="flex justify-center">
          <div class="mb-3 xl:w-96">
            <label
              for="exampleText0"
              class="form-label inline-block mb-2 text-gray-700"
            >
              Article Title
            </label>
            <input
              type="text"
              class="
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
              name="title"
              id="title"
              placeholder="Article Title"
              onChange={handleChange}
            />
          </div>
        </div>

        <div class="flex justify-center">
          <div class="mb-3 xl:w-96">
            <label
              for="exampleText0"
              class="form-label inline-block mb-2 text-gray-700"
            >
              Article Description
            </label>
            <input
              type="text"
              name="description"
              class="
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
              id="description"
              placeholder="Article Description"
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="flex justify-center">
          <div className="mb-3 xl:w-96">
            <label
              //   for="exampleFormControlTextarea1"
              className="form-label inline-block mb-2 text-gray-700"
            >
              Example textarea
            </label>
            <textarea
              onChange={(e) => {
                setMd(e.target.value);
                handleChange(e);
              }}
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
            ></textarea>
          </div>
        </div>
        <div className="flex justify-center">
          <button
            id="preview"
            onClick={onPreviewClick}
            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Preview
          </button>
          <button
            id="publish"
            onClick={onSaveClick}
            className="p-5 inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Publish
          </button>
        </div>
      </div>
      {showPreview && (
        <div className="article-wrapper padding-2 shadow-md">
          <article>
            <main>
              <ReactMarkdown>{md}</ReactMarkdown>
            </main>
          </article>
        </div>
      )}
    </div>
  );
}
