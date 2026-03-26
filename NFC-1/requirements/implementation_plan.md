# NFC Card Writer Implementation Plan

This project aims to create a Python application that encodes contact details or other information onto an NFC card. When an NFC-enabled mobile phone taps this card, the details are instantly shared.

> [!NOTE]
> NFC tags are passive storage mediums and cannot "run" a Python script directly. Our Python application will run on your computer to **write** the NDEF data payload directly onto the NFC tag using a USB NFC Reader/Writer.

## User Review Required
Before we start coding, please clarify a couple of details:
1. **Hardware**: Do you have a USB NFC Reader/Writer (like the ACS ACR122U) available to attach to your computer to write the cards?
2. **Payload Type**: Which format do you prefer for sharing details?
   - **Option A (vCard)**: The contact details are stored directly on the NFC card using the vCard format. The phone taps the card and immediately prompts the user to "Save to Contacts". (Note: Requires a card with sufficient memory, e.g., NTAG215 or NTAG216).
   - **Option B (URL)**: The NFC card simply stores a web URL pointing to an online profile (like Linktree, a hosted digital business card, etc). This works with cheaper/smaller cards like the NTAG213 and makes updating the details later much easier (since you just change the website).

## Proposed Architecture & Workflow

### 1. Dependencies
- **`nfcpy`**: For interfacing with the USB NFC Reader/Writer hardware from Python.
- **`ndeflib`**: For formatting the data payload into NDEF (NFC Data Exchange Format), which is the standard format a mobile phone expects.

### 2. Application Flow
- **Input**: The Python script prompts the user for contact details (Name, Phone, Email, etc.) and gathers the target info.
- **Processing**: The application converts this data into an standard NDEF Record format (either URI or vCard).
- **Writing**: The application establishes a connection to the local NFC hardware. The user places the blank NFC card on the reader, and the application transfers and writes the NDEF data into the card.

### 3. File Structure
We will create these files under the `NFC-1` folder:

#### [NEW] `requirements.txt`(file:///Users/puppalakarthik/PycharmProjects/pilotPython/pilotPython/NFC/NFC-1/requirements.txt)
#### [NEW] `payload_generator.py`(file:///Users/puppalakarthik/PycharmProjects/pilotPython/pilotPython/NFC/NFC-1/payload_generator.py)
#### [NEW] `nfc_writer.py`(file:///Users/puppalakarthik/PycharmProjects/pilotPython/pilotPython/NFC/NFC-1/nfc_writer.py)
#### [NEW] `main.py`(file:///Users/puppalakarthik/PycharmProjects/pilotPython/pilotPython/NFC/NFC-1/main.py)

## Verification Plan

### Automated Tests
- We'll write basic sanity tests to ensure our NDEF message payloads are generated and encoded correctly without hardware required.

### Manual Verification
- We will run `main.py`, place an NFC tag on the USB reader, and verify our script reports a successful write.
- We will then grab an iOS or Android smartphone, enable NFC, tap the written card, and confirm the contact prompt or URL pop-up works smoothly.
