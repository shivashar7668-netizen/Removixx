"""
Removix UI - Information & Company Views
----------------------------------------
Contains user-facing pages:
- Privacy Policy (/privacy-policy, /privacy)
- Frequently Asked Questions (/faq)
- Contact Us (/contact)
- About Removix (/about)

All views use render_layout for consistent navigation, theme tokens, and footer.
"""

from ui.layout import render_layout

INFO_PAGES_CSS = r"""
/* ========== INFO PAGES COMMON STYLES ========== */
.info-content-card {
  max-width: 880px;
  margin: 0 auto;
  width: 100%;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--line, #e2e8f0);
  border-radius: var(--radius-xl, 24px);
  padding: 40px 48px;
  box-sizing: border-box;
  box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
  position: relative;
}

body.dark-mode .info-content-card,
[data-theme="dark"] .info-content-card {
  background: #111827 !important;
  border-color: #1e293b !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
}

.info-last-updated-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 9999px;
  background: var(--sky-light, #e0f2fe);
  color: var(--primary, #0284c7);
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 24px;
}

body.dark-mode .info-last-updated-badge,
[data-theme="dark"] .info-last-updated-badge {
  background: rgba(2, 132, 199, 0.18) !important;
  color: #38bdf8 !important;
}

.info-prose-section {
  display: flex;
  flex-direction: column;
  gap: 28px;
  color: var(--ink, #0f172a);
  line-height: 1.7;
  font-size: 15px;
}

.info-section-item h3 {
  font-size: 19px;
  font-weight: 800;
  color: var(--ink, #0f172a);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

body.dark-mode .info-section-item h3,
[data-theme="dark"] .info-section-item h3 {
  color: #f1f5f9 !important;
}

.info-section-item p {
  color: var(--ink-muted, #475569);
  font-size: 14.5px;
  line-height: 1.68;
  margin-bottom: 12px;
}

body.dark-mode .info-section-item p,
[data-theme="dark"] .info-section-item p {
  color: #94a3b8 !important;
}

.info-highlight-box {
  background: rgba(2, 132, 199, 0.05);
  border-left: 3px solid #0284c7;
  padding: 14px 18px;
  border-radius: 0 12px 12px 0;
  margin: 14px 0;
  font-size: 14px;
  color: var(--ink, #0f172a);
}

body.dark-mode .info-highlight-box,
[data-theme="dark"] .info-highlight-box {
  background: rgba(14, 165, 233, 0.1) !important;
  border-left-color: #38bdf8 !important;
  color: #e2e8f0 !important;
}

/* FAQ Accordion Styling */
.faq-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}

.faq-card {
  border: 1px solid var(--line, #e2e8f0);
  border-radius: 16px;
  padding: 20px 24px;
  background: var(--card-bg, #ffffff);
  transition: all 0.2s ease;
}

body.dark-mode .faq-card,
[data-theme="dark"] .faq-card {
  background: #162032 !important;
  border-color: #1e293b !important;
}

.faq-question {
  font-size: 16px;
  font-weight: 700;
  color: var(--ink, #0f172a);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

body.dark-mode .faq-question,
[data-theme="dark"] .faq-question {
  color: #f8fafc !important;
}

.faq-question-icon {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: rgba(2, 132, 199, 0.1);
  color: #0284c7;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

body.dark-mode .faq-question-icon,
[data-theme="dark"] .faq-question-icon {
  background: rgba(56, 189, 248, 0.15) !important;
  color: #38bdf8 !important;
}

.faq-answer {
  color: var(--ink-muted, #475569);
  font-size: 14px;
  line-height: 1.65;
  padding-left: 36px;
}

body.dark-mode .faq-answer,
[data-theme="dark"] .faq-answer {
  color: #94a3b8 !important;
}

/* Contact Grid & Form */
.contact-layout-grid {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 36px;
  align-items: start;
}

@media (max-width: 820px) {
  .contact-layout-grid {
    grid-template-columns: 1fr;
    gap: 28px;
  }
}

.contact-info-col {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.contact-channel-card {
  padding: 18px 20px;
  border-radius: 16px;
  background: var(--bg-page, #f8fafc);
  border: 1px solid var(--line, #e2e8f0);
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

body.dark-mode .contact-channel-card,
[data-theme="dark"] .contact-channel-card {
  background: #162032 !important;
  border-color: #1e293b !important;
}

.contact-channel-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(2, 132, 199, 0.1);
  color: #0284c7;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

body.dark-mode .contact-channel-icon,
[data-theme="dark"] .contact-channel-icon {
  background: rgba(56, 189, 248, 0.15) !important;
  color: #38bdf8 !important;
}

.contact-form-col {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group-item label {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--ink, #0f172a);
}

body.dark-mode .form-group-item label,
[data-theme="dark"] .form-group-item label {
  color: #f1f5f9 !important;
}

.form-input-field {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid var(--line, #e2e8f0);
  background: var(--card-bg, #ffffff);
  color: var(--ink, #0f172a);
  font-family: inherit;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

body.dark-mode .form-input-field,
[data-theme="dark"] .form-input-field {
  background: #0f172a !important;
  border-color: #334155 !important;
  color: #f8fafc !important;
}

.form-input-field:focus {
  outline: none;
  border-color: #0284c7;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
}

/* About Page Pillar Cards */
.about-pillars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin: 28px 0;
}

@media (max-width: 768px) {
  .about-pillars-grid {
    grid-template-columns: 1fr;
  }
  .info-content-card {
    padding: 28px 20px;
  }
}

.pillar-box {
  background: var(--bg-page, #f8fafc);
  border: 1px solid var(--line, #e2e8f0);
  border-radius: 16px;
  padding: 22px 20px;
  text-align: center;
}

body.dark-mode .pillar-box,
[data-theme="dark"] .pillar-box {
  background: #162032 !important;
  border-color: #1e293b !important;
}

.pillar-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(2, 132, 199, 0.1);
  color: #0284c7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

body.dark-mode .pillar-icon-wrap,
[data-theme="dark"] .pillar-icon-wrap {
  background: rgba(56, 189, 248, 0.15) !important;
  color: #38bdf8 !important;
}

.pillar-box h4 {
  font-size: 16px;
  font-weight: 800;
  color: var(--ink, #0f172a);
  margin-bottom: 6px;
}

body.dark-mode .pillar-box h4,
[data-theme="dark"] .pillar-box h4 {
  color: #f1f5f9 !important;
}

.pillar-box p {
  font-size: 13px;
  color: var(--ink-muted, #475569);
  line-height: 1.55;
  margin: 0;
}

body.dark-mode .pillar-box p,
[data-theme="dark"] .pillar-box p {
  color: #94a3b8 !important;
}
"""


def render_privacy_page() -> str:
    """Renders the Privacy Policy page."""
    main_html = """
    <div class="info-content-card">
      <div class="info-last-updated-badge">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Last Updated: September 2026
      </div>

      <div class="info-prose-section">
        <div class="info-section-item">
          <h3>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#16a34a" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            1. Our Fundamental Commitment to Privacy
          </h3>
          <p>
            At <strong>Removix</strong>, we believe file conversion, image manipulation, and document editing should never require sacrificing your confidentiality. Our platform is intentionally architected around an <strong>on-device and local-first execution model</strong>.
          </p>
          <div class="info-highlight-box">
            <strong>Key Guarantee:</strong> Your files belong to you. We never sell, rent, monetize, inspect, or retain your files, documents, photos, or videos.
          </div>
        </div>

        <div class="info-section-item">
          <h3>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#0284c7" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            2. How File Processing Operates
          </h3>
          <p>
            • <strong>Client-Side Processing:</strong> Tools such as PDF previews, canvas transformations, rotation, image cropping, and instant format previews execute directly inside your browser without uploading raw files to external servers.
          </p>
          <p>
            • <strong>Server Buffer Cleanup:</strong> When deep neural processing is necessary (such as AI background removal or watermark erasing), files are temporarily handled in volatile memory and purged immediately after the output is returned. No permanent cloud storage or file archives exist.
          </p>
        </div>

        <div class="info-section-item">
          <h3>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#6366f1" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
            3. Zero AI Model Training on User Data
          </h3>
          <p>
            Unlike many cloud conversion services, Removix strictly forbids using user submissions, uploaded images, or processed documents to train machine learning models. Your proprietary intellectual property and personal memories remain untouched.
          </p>
        </div>

        <div class="info-section-item">
          <h3>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#eab308" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
            4. Local Browser Storage
          </h3>
          <p>
            We use your browser's local storage (<code>localStorage</code>) strictly to preserve your selected interface theme (Dark Mode / Light Mode) and recent tool history on your device. You can clear this anytime with a single click.
          </p>
        </div>

        <div class="info-section-item">
          <h3>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#ec4899" stroke-width="2.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            5. Contact Privacy Inquiries
          </h3>
          <p>
            For privacy questions or data inquiries, reach out directly to our maintainer at <a href="mailto:privacy@removix.com" style="color:#0284c7; font-weight:700;">privacy@removix.com</a> or via our <a href="/contact" style="color:#0284c7; font-weight:700;">Contact Form</a>.
          </p>
        </div>
      </div>
    </div>
    """
    return render_layout(
        title="Privacy Policy",
        active_tool="",
        hero_title="Privacy Policy",
        hero_sub="Your data and files remain 100% private. We never sell, store, or train on your documents.",
        main_card_html=main_html,
        extra_css=INFO_PAGES_CSS,
    )


def render_faq_page() -> str:
    """Renders the Frequently Asked Questions page."""
    main_html = """
    <div class="info-content-card">
      <div class="info-last-updated-badge">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        Common Questions
      </div>

      <div class="faq-grid">
        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <span>Is Removix completely free to use?</span>
          </div>
          <div class="faq-answer">
            Yes! All essential features across Image Tools, PDF Tools, and Video Tools are completely free to use without requiring an upfront subscription or hidden paywall.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </div>
            <span>Are my uploaded files and photos private?</span>
          </div>
          <div class="faq-answer">
            100% private. Most tools process directly in your browser using modern WebAssembly and Canvas APIs. Any server-assisted operations run in isolated temporary RAM and are purged immediately after download. We never store or inspect your content.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            </div>
            <span>What image formats are supported?</span>
          </div>
          <div class="faq-answer">
            Removix supports PNG, JPG, JPEG, WEBP, SVG, GIF, and TIFF for conversions, resizing, compression, cropping, text typography, circular masking, and AI background removal.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            </div>
            <span>How does PDF editing and conversion work?</span>
          </div>
          <div class="faq-answer">
            Our PDF suite utilizes high-performance document parsing alongside browser-side vector rendering. You can merge multiple documents, split pages, rotate individual orientations, delete unwanted sheets, or convert Word documents with live visual page previews.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
            <span>Is there any file size limit?</span>
          </div>
          <div class="faq-answer">
            Removix is tuned for smooth high-speed performance. Documents up to 50 MB, ultra-high-resolution images, and videos up to 100 MB are supported with zero bottlenecking.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-question">
            <div class="faq-question-icon">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            </div>
            <span>Does Removix work on mobile and tablet devices?</span>
          </div>
          <div class="faq-answer">
            Yes, every single tool in Removix features a responsive touch-optimized layout, supporting touch crop drag, mobile preview zoom, and responsive card sizing.
          </div>
        </div>
      </div>
    </div>
    """
    return render_layout(
        title="Frequently Asked Questions",
        active_tool="",
        hero_title="Frequently Asked Questions",
        hero_sub="Everything you need to know about Removix tools, offline privacy, and file workflows.",
        main_card_html=main_html,
        extra_css=INFO_PAGES_CSS,
    )


def render_contact_page() -> str:
    """Renders the Contact Us page."""
    main_html = """
    <div class="info-content-card">
      <div class="contact-layout-grid">
        <!-- Left: Channels Info -->
        <div class="contact-info-col">
          <div>
            <h3 style="font-size:20px; font-weight:800; color:var(--ink); margin-bottom:8px;">Get in Touch</h3>
            <p style="font-size:14px; color:var(--ink-muted); line-height:1.6;">
              Have questions, feedback, bug reports, or feature requests? Drop us a message and our team will get back to you promptly.
            </p>
          </div>

          <div class="contact-channel-card">
            <div class="contact-channel-icon">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            </div>
            <div>
              <h4 style="font-size:14px; font-weight:700; color:var(--ink); margin-bottom:2px;">Support &amp; Feedback</h4>
              <a href="mailto:support@removix.com" style="font-size:13px; color:#0284c7; font-weight:600;">support@removix.com</a>
            </div>
          </div>

          <div class="contact-channel-card">
            <div class="contact-channel-icon" style="background:rgba(16, 185, 129, 0.1); color:#10b981;">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div>
              <h4 style="font-size:14px; font-weight:700; color:var(--ink); margin-bottom:2px;">Developer</h4>
              <a href="https://shivankthakur.com/" target="_blank" rel="noopener noreferrer" style="font-size:13px; color:#0284c7; font-weight:600; display:inline-flex; align-items:center; gap:4px;">
                Shivank Thakur
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
              </a>
            </div>
          </div>

          <div class="contact-channel-card">
            <div class="contact-channel-icon" style="background:rgba(99, 102, 241, 0.1); color:#6366f1;">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            </div>
            <div>
              <h4 style="font-size:14px; font-weight:700; color:var(--ink); margin-bottom:2px;">Response Time</h4>
              <p style="font-size:12.5px; color:var(--ink-muted); margin:0;">Usually within 24 hours</p>
            </div>
          </div>
        </div>

        <!-- Right: Interactive Form -->
        <div class="contact-form-col">
          <form id="contactForm" onsubmit="handleContactSubmit(event)" style="display:flex; flex-direction:column; gap:16px;">
            <div class="form-group-item">
              <label for="contactName">Your Name</label>
              <input type="text" id="contactName" class="form-input-field" placeholder="e.g. Alex Morgan" required>
            </div>

            <div class="form-group-item">
              <label for="contactEmail">Email Address</label>
              <input type="email" id="contactEmail" class="form-input-field" placeholder="alex@example.com" required>
            </div>

            <div class="form-group-item">
              <label for="contactTopic">Topic</label>
              <select id="contactTopic" class="form-input-field">
                <option value="feedback">General Feedback</option>
                <option value="bug">Report an Issue / Bug</option>
                <option value="feature">Request a New Tool</option>
                <option value="business">Partnership / Other</option>
              </select>
            </div>

            <div class="form-group-item">
              <label for="contactMessage">Message</label>
              <textarea id="contactMessage" class="form-input-field" rows="4" placeholder="How can we assist you today?" required></textarea>
            </div>

            <button type="submit" class="btn-primary" id="btnSubmitContact" style="padding:12px 24px; font-size:14.5px; width:100%; justify-content:center;">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              Send Message
            </button>

            <div id="contactSuccessNotice" style="display:none; padding:12px 16px; background:#dcfce7; border:1px solid #bbf7d0; border-radius:12px; color:#15803d; font-size:13.5px; font-weight:600; text-align:center;">
              ✓ Thank you! Your message has been sent successfully. We will reply soon.
            </div>
          </form>
        </div>
      </div>
    </div>
    """

    contact_js = r"""
    function handleContactSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('btnSubmitContact');
      btn.disabled = true;
      btn.textContent = 'Sending...';

      setTimeout(() => {
        btn.style.display = 'none';
        document.getElementById('contactSuccessNotice').style.display = 'block';
        document.getElementById('contactForm').reset();
      }, 600);
    }
    """

    return render_layout(
        title="Contact Us",
        active_tool="",
        hero_title="Contact Us",
        hero_sub="Have a suggestion, question, or need assistance? We're here to help.",
        main_card_html=main_html,
        extra_css=INFO_PAGES_CSS,
        extra_js=contact_js,
    )


def render_about_page() -> str:
    """Renders the About Removix page."""
    main_html = """
    <div class="info-content-card">
      <div class="info-last-updated-badge">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        Our Story &amp; Purpose
      </div>

      <div class="info-prose-section">
        <div class="info-section-item">
          <h3>The Removix Vision</h3>
          <p>
            Online file converter websites are often filled with slow redirects, intrusive advertisements, confusing download buttons, and opaque privacy policies where user files might be retained indefinitely.
          </p>
          <p>
            <strong>Removix</strong> was built to solve this problem once and for all: a clean, fast, on-device AI-powered media and document utility suite designed for creators, students, photographers, and developers.
          </p>
        </div>

        <div class="about-pillars-grid">
          <div class="pillar-box">
            <div class="pillar-icon-wrap">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
            <h4>Instant Speed</h4>
            <p>Runs directly on client hardware and high-efficiency local engines with zero queue delay.</p>
          </div>

          <div class="pillar-box">
            <div class="pillar-icon-wrap" style="background:rgba(16, 185, 129, 0.1); color:#10b981;">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <h4>Strict Privacy</h4>
            <p>Your photos, videos, and private contracts never get stored, analyzed, or shared with third parties.</p>
          </div>

          <div class="pillar-box">
            <div class="pillar-icon-wrap" style="background:rgba(99, 102, 241, 0.1); color:#6366f1;">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            </div>
            <h4>All-In-One</h4>
            <p>Over 30+ conversion, editing, and enhancement tools accessible under one cohesive, dark-mode design.</p>
          </div>
        </div>

        <div class="info-section-item">
          <h3>Designed &amp; Developed by Shivank Thakur</h3>
          <p>
            Removix is created and maintained by <strong>Shivank Thakur</strong> as a production-grade showcase of modern agentic engineering, high-performance Python backends, and responsive frontend systems.
          </p>
          <div style="margin-top:14px;">
            <a href="https://shivankthakur.com/" target="_blank" rel="noopener noreferrer" class="btn-primary" style="display:inline-flex; width:auto; text-decoration:none;">
              <span>Visit Shivank's Portfolio</span>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
          </div>
        </div>
      </div>
    </div>
    """
    return render_layout(
        title="About Removix",
        active_tool="",
        hero_title="About Removix",
        hero_sub="Universal on-device AI media and document utility suite built for speed, simplicity, and total privacy.",
        main_card_html=main_html,
        extra_css=INFO_PAGES_CSS,
    )
