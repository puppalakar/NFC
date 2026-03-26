# NFC Application Requirements Analysis

Before building the application, it's crucial to understand how modern NFC (Near Field Communication) systems interact, particularly between passive tags, a desktop application, and mobile smartphones.

## 1. The Core Architecture

The system involves three main components:
1. **The Writer (Your Computer + USB Reader):** A Python application writes data to a blank card.
2. **The Medium (NFC Card/Tag):** A passive, battery-less chip that stores data.
3. **The Reader (Smartphone):** A mobile phone that powers the tag upon tapping and reads the data automatically.

---

## 2. Hardware Requirements

### A. NFC Reader/Writer (For the Computer)
Your computer does not have a built-in NFC writer capable of programming cards for this use case. You will need external hardware.
* **Component needed:** A USB NFC Reader/Writer.
* **Industry Standard:** **ACS ACR122U** (approx. $30-$40). It has strong support in Python and OS drivers (macOS, Windows, Linux).
* **Purpose:** To pair with your Python app to physically write to the cards.

### B. NFC Tags/Cards
The actual physical cards your users will tap. Not all cards are identical; they have different memory limits.
* **NTAG213 (144 bytes):** Cheap. Great for just storing a URL. Too small for a full vCard (direct contact save).
* **NTAG215 (504 bytes):** Medium size (and the standard for Nintendo Amiibos). Can fit a minimal vCard.
* **NTAG216 (888 bytes):** Best choice if you intend to store full Contact Details (vCard) with names, multiple phone numbers, and addresses directly on the card.

---

## 3. Software Requirements

### Python Libraries needed on Desktop
To talk to the hardware and format the data properly, the Python application will need:
* **`nfcpy`**: The driver layer. Allows Python to detect when a card is placed on the USB reader and transmit signals to it.
* **`ndeflib`**: The data formatter. NFC tags hold data in blocks. For a smartphone to understand what the data is (e.g., "this is a contact," or "this is a website"), it must be encoded in the **NDEF (NFC Data Exchange Format)** structure.

---

## 4. Payload Approach (Crucial Decision)

How do you want to share the details when the mobile taps the card?

### Option A: The vCard Approach (Direct Save)
* **How it works:** The Python app encodes a `vCard` (a standardized virtual contact file) onto the tag.
* **User Experience:** An iPhone or Android user taps the card, and their phone immediately opens the "New Contact" screen pre-filled with the details, ready to save.
* **Pros:** Works entirely offline; no internet connection needed by the mobile phone.
* **Cons:** Hard limit on file size (can't have a profile photo easily, constrained by tag memory). If details change, you must physically rewrite the card.

### Option B: The Cloud/URL Approach 
* **How it works:** The Python app writes a single URL onto the tag (e.g., `https://yourdomain.com/user/karthik`).
* **User Experience:** The user taps the card, their phone prompts to open Safari/Chrome, and it loads a sleek web profile. That webpage can have a "Download Contact" button that provides the vCard.
* **Pros:** 
  * You can use the cheapest NTAG213 tags.
  * You can remotely update the person's phone number online without having to touch the physical card again.
  * Richer experience (profile photos, dynamic links).
* **Cons:** Requires the tapped smartphone to have internet access.

---

## 5. Mobile OS Caveats
* **iOS (Apple):** iPhones (iPhone XS and newer) natively read NDEF formatted tags in the background. If you encode the tag properly using NDEF containing a URI or vCard, iOS handles it automatically without an app.
* **Android:** Most modern Androids will seamlessly prompt to open a URL or save a vCard when scanning an NDEF formatted tag.
