// Simple script to test JWT token decoding
function decodeToken(token) {
  if (!token) {
    console.log("No token provided");
    return null;
  }

  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      console.log("Invalid token format");
      return null;
    }

    const payload = parts[1];
    const decodedPayload = atob(payload);
    const parsedPayload = JSON.parse(decodedPayload);

    console.log("Decoded token payload:", parsedPayload);
    console.log("User ID from token:", parsedPayload.user_id);
    return parsedPayload.user_id;
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
}

// Example token for testing (replace with a real token from localStorage if available)
// This is just a placeholder to test the function
console.log("Testing token decoding function...");
// decodeToken("your_actual_token_here"); // Uncomment and replace with actual token to test