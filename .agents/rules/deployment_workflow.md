# Deployment & Backup Standard Operating Procedure

## 1. Local Development & Real-Time Preview
- All editing happens locally on the machine.
- Local previews/servers are kept active so changes can be viewed in real-time on the display layout.
- Edits remain strictly local during the design and development phase.

## 2. Mandatory Approval Barrier for Live Deployment
- **NEVER** push to the live hosting platform (Namecheap) without explicit user approval.
- An update can ONLY be pushed to Namecheap if:
  a) The user explicitly commands it (e.g., *'Go ahead and push to live'*), OR
  b) Antigravity asks (*'Would you like to deploy these approved changes live?'*) and the user explicitly answers **Yes**.
- Without one of these two confirmations, live files on Namecheap must never be touched.

## 3. Two-Stage Deployment & Automatic Backup Chain
When approved, execution MUST proceed in this exact two-stage sequence:
1. **Stage 1 (Live Push to Namecheap)**:
   - Push updated files to Namecheap hosting (
amecheap-gateway:public_html/).
   - Verify that the transfer completed successfully.
2. **Stage 2 (Automatic GitHub Backup)**:
   - **Trigger**: Only after Stage 1 completes successfully.
   - **Behavior**: Run immediately and automatically without asking for a separate confirmation (*'If Namecheap gets it, GitHub gets it too, every single time'*).
   - Commit all changes and push directly to GitHub (origin main -> https://github.com/dessec/gateway_website.git).
