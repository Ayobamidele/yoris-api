/**
 * ============================================================
 *  YORIS API — Postman Test Scripts
 * ============================================================
 * These scripts are already embedded inside yoris_api.postman_collection.json.
 * This file is a readable reference so you can copy-paste individual
 * test blocks into any Postman request's "Tests" tab.
 *
 * COLLECTION VARIABLES (auto-set at runtime):
 *   baseUrl    — http://127.0.0.1:8000
 *   userId     — set after "Create User 1"
 *   userId2    — set after "Create User 2"
 *   postId     — set after "Create Post"
 *   commentId  — set after "Create Comment"
 *   deliveryId — set after "Create Delivery"
 *
 * RUN ORDER (Collection Runner):
 *   1.  Health Check
 *   2.  Create User 1
 *   3.  Create User 2
 *   4.  Get All Users
 *   5.  Get User By ID
 *   6.  Get User By ID - Not Found
 *   7.  Create Post
 *   8.  Create Post - Invalid userId
 *   9.  Get All Posts
 *   10. Get Post By ID
 *   11. Get Post By ID - Not Found
 *   12. Create Comment
 *   13. Create Comment - Invalid postId
 *   14. Get All Comments
 *   15. Get Comment By ID
 *   16. Get Comment By ID - Not Found
 *   17. Get Wallet by User ID
 *   18. Get Wallet - Not Found
 *   19. Transfer Funds
 *   20. Transfer Funds - Insufficient Balance
 *   21. Transfer Funds - Sender Not Found
 *   22. Create Delivery
 *   23. Create Delivery - User Not Found
 *   24. Create Delivery - Post Not Found
 *   25. Mock Error - 400
 *   26. Mock Error - 500
 * ============================================================
 */

/* ──────────────────────────────────────────────
   1. GET /health
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Status is ok", () => {
    const json = pm.response.json();
    pm.expect(json.status).to.eql("ok");
});


/* ──────────────────────────────────────────────
   2. POST /users/  (Create User 1)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "name": "Alice", "username": "alice99", "email": "alice@example.com" }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("User has id", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json.name).to.eql("Alice");
    pm.collectionVariables.set("userId", json.id);
});


/* ──────────────────────────────────────────────
   3. POST /users/  (Create User 2 — transfer target)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "name": "Bob", "username": "bobby42", "email": "bob@example.com" }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("User 2 has id", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.collectionVariables.set("userId2", json.id);
});


/* ──────────────────────────────────────────────
   4. GET /users/
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Response is array", () => {
    pm.expect(pm.response.json()).to.be.an("array");
});


/* ──────────────────────────────────────────────
   5. GET /users/{{userId}}
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Correct user returned", () => {
    const json = pm.response.json();
    pm.expect(json.id).to.eql(parseInt(pm.collectionVariables.get("userId")));
});


/* ──────────────────────────────────────────────
   6. GET /users/999999  (Not Found)
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 404", () => pm.response.to.have.status(404));
pm.test("Detail message present", () => {
    pm.expect(pm.response.json().detail).to.eql("User not found");
});


/* ──────────────────────────────────────────────
   7. POST /posts/  (Create Post)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "userId": {{userId}}, "title": "My First Post", "body": "Hello Yoris world!", "amount": 49.99 }

// PRE-REQUEST TAB
const uid = pm.collectionVariables.get("userId");
if (!uid) { throw new Error("userId not set — run Create User first"); }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Post has id", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json.title).to.eql("My First Post");
    pm.collectionVariables.set("postId", json.id);
});


/* ──────────────────────────────────────────────
   8. POST /posts/  (Invalid userId)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "userId": 999999, "title": "Ghost Post", "body": "This should fail", "amount": 10.00 }

// TESTS TAB
pm.test("Status 400 for bad userId", () => pm.response.to.have.status(400));
pm.test("Detail mentions userId", () => {
    pm.expect(pm.response.json().detail).to.include("userId");
});


/* ──────────────────────────────────────────────
   9. GET /posts/
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Response is array", () => {
    pm.expect(pm.response.json()).to.be.an("array");
});


/* ──────────────────────────────────────────────
   10. GET /posts/{{postId}}
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Correct post returned", () => {
    const json = pm.response.json();
    pm.expect(json.id).to.eql(parseInt(pm.collectionVariables.get("postId")));
});


/* ──────────────────────────────────────────────
   11. GET /posts/999999  (Not Found)
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 404", () => pm.response.to.have.status(404));
pm.test("Detail is Post not found", () => {
    pm.expect(pm.response.json().detail).to.eql("Post not found");
});


/* ──────────────────────────────────────────────
   12. POST /comments/  (Create Comment)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "name": "Alice", "email": "alice@example.com", "body": "Great post!", "postId": {{postId}} }

// PRE-REQUEST TAB
const pid = pm.collectionVariables.get("postId");
if (!pid) { throw new Error("postId not set — run Create Post first"); }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Comment has id", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.collectionVariables.set("commentId", json.id);
});


/* ──────────────────────────────────────────────
   13. POST /comments/  (Invalid postId)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "name": "Ghost", "email": "ghost@example.com", "body": "This should fail", "postId": 999999 }

// TESTS TAB
pm.test("Status 400 for bad postId", () => pm.response.to.have.status(400));
pm.test("Detail mentions postId", () => {
    pm.expect(pm.response.json().detail).to.include("postId");
});


/* ──────────────────────────────────────────────
   14. GET /comments/
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Response is array", () => {
    pm.expect(pm.response.json()).to.be.an("array");
});


/* ──────────────────────────────────────────────
   15. GET /comments/{{commentId}}
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Correct comment returned", () => {
    const json = pm.response.json();
    pm.expect(json.id).to.eql(parseInt(pm.collectionVariables.get("commentId")));
});


/* ──────────────────────────────────────────────
   16. GET /comments/999999  (Not Found)
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 404", () => pm.response.to.have.status(404));
pm.test("Detail is Comment not found", () => {
    pm.expect(pm.response.json().detail).to.eql("Comment not found");
});


/* ──────────────────────────────────────────────
   17. GET /wallet/{{userId}}
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Wallet has balance and userId", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("balance");
    pm.expect(json.userId).to.eql(parseInt(pm.collectionVariables.get("userId")));
    pm.expect(json.balance).to.eql(1000);
});


/* ──────────────────────────────────────────────
   18. GET /wallet/999999  (Not Found)
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 404", () => pm.response.to.have.status(404));
pm.test("Detail is Wallet not found", () => {
    pm.expect(pm.response.json().detail).to.eql("Wallet not found");
});


/* ──────────────────────────────────────────────
   19. POST /wallet/transfer  (Happy Path)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "senderId": {{userId}}, "receiverId": {{userId2}}, "amount": 250 }

// PRE-REQUEST TAB
const u1 = pm.collectionVariables.get("userId");
const u2 = pm.collectionVariables.get("userId2");
if (!u1 || !u2) { throw new Error("userId or userId2 not set — run Create User steps first"); }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Transfer successful message", () => {
    const json = pm.response.json();
    pm.expect(json.message).to.eql("Transfer successful");
    pm.expect(json).to.have.property("sender_balance");
    pm.expect(json.sender_balance).to.eql(750); // 1000 - 250
});


/* ──────────────────────────────────────────────
   20. POST /wallet/transfer  (Insufficient Balance)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "senderId": {{userId}}, "receiverId": {{userId2}}, "amount": 9999999 }

// TESTS TAB
pm.test("Status 402 for insufficient balance", () => pm.response.to.have.status(402));
pm.test("Detail mentions Insufficient balance", () => {
    pm.expect(pm.response.json().detail).to.include("Insufficient balance");
});


/* ──────────────────────────────────────────────
   21. POST /wallet/transfer  (Sender Not Found)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "senderId": 888888, "receiverId": {{userId2}}, "amount": 10 }

// TESTS TAB
pm.test("Status 404 for missing sender", () => pm.response.to.have.status(404));
pm.test("Detail mentions Sender wallet", () => {
    pm.expect(pm.response.json().detail).to.include("Sender wallet not found");
});


/* ──────────────────────────────────────────────
   22. POST /users/{{userId}}/deliveries  (Create Delivery)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "post_id": {{postId}} }

// PRE-REQUEST TAB
const uid2 = pm.collectionVariables.get("userId");
const pid2 = pm.collectionVariables.get("postId");
if (!uid2 || !pid2) { throw new Error("userId or postId not set — run Users + Posts steps first"); }

// TESTS TAB
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Delivery created with id", () => {
    const json = pm.response.json();
    pm.expect(json.message).to.eql("Delivery created");
    pm.expect(json).to.have.property("delivery_id");
    pm.expect(json.rider_status).to.eql("BUSY");
    pm.collectionVariables.set("deliveryId", json.delivery_id);
});


/* ──────────────────────────────────────────────
   23. POST /users/999999/deliveries  (User Not Found)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "post_id": {{postId}} }

// TESTS TAB
pm.test("Status 404 for missing user", () => pm.response.to.have.status(404));
pm.test("Detail is User not found", () => {
    pm.expect(pm.response.json().detail).to.eql("User not found");
});


/* ──────────────────────────────────────────────
   24. POST /users/{{userId}}/deliveries  (Post Not Found)
   ────────────────────────────────────────────── */
// REQUEST BODY:
// { "post_id": 999999 }

// TESTS TAB
pm.test("Status 404 for missing post", () => pm.response.to.have.status(404));
pm.test("Detail is Post not found", () => {
    pm.expect(pm.response.json().detail).to.eql("Post not found");
});


/* ──────────────────────────────────────────────
   25. GET /test/error/400
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 400", () => pm.response.to.have.status(400));
pm.test("Error body mocks status", () => {
    pm.expect(pm.response.json().error).to.include("400");
});


/* ──────────────────────────────────────────────
   26. GET /test/error/500
   ────────────────────────────────────────────── */
// TESTS TAB
pm.test("Status 500", () => pm.response.to.have.status(500));
pm.test("Error body mocks status", () => {
    pm.expect(pm.response.json().error).to.include("500");
});
