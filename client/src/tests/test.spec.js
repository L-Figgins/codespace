describe("Always pass test for CI pipeline testings", () => {
  it("should always pass", () => {
    expect(1 + 1).toBe(2);
  });

  it("should fail", () => {
    expect(1 + 1).toBe(3);
  });
});
