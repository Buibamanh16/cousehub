import { describe, it } from "node:test";
import assert from "node:assert/strict";

function buildApiUrl(baseUrl, path) {
  const cleanBase = (baseUrl || "/api").replace(/\/+$/, "");
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${cleanBase}${cleanPath}`;
}

describe("Frontend API URL configuration", () => {
  it("uses /api prefix by default for Nginx reverse proxy", () => {
    assert.equal(buildApiUrl(undefined, "/sections"), "/api/sections");
    assert.equal(buildApiUrl("/api", "enrollments"), "/api/enrollments");
  });

  it("strips trailing slash from custom base URL cleanly", () => {
    assert.equal(
      buildApiUrl("http://127.0.0.1:8000/", "/health"),
      "http://127.0.0.1:8000/health",
    );
  });
});
