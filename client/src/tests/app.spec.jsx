import renderer from "react-test-renderer";
import App from "../App";

describe("App.js", () => {
  it("should render", () => {
    const component = renderer.create(<App></App>);
    let tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
