"""
Removix UI - Profile Page View
------------------------------
User profile and account management view connected to Supabase Auth.
"""

from ui.layout import render_layout
from modules.auth_config import get_supabase_config

PROFILE_CSS = r"""
/* ========== PROFILE PAGE STYLES ========== */
.profile-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1140px;
  margin: 0 auto;
  width: 100%;
}

.profile-card {
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg, 16px);
  padding: 28px 32px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
}

body.dark-mode .profile-card {
  background: #162032;
  border-color: #1e293b;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.profile-header-row {
  display: flex;
  align-items: center;
  gap: 22px;
}

.profile-avatar-large {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  color: #ffffff;
  font-size: 28px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
  flex-shrink: 0;
}

.profile-title-group h2 {
  font-size: 22px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.profile-badges-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.profile-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.badge-active {
  background: #dcfce7;
  color: #15803d;
}

body.dark-mode .badge-active {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
}

.badge-supabase {
  background: #e0f2fe;
  color: #0284c7;
}

body.dark-mode .badge-supabase {
  background: rgba(14, 165, 233, 0.15);
  color: #38bdf8;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 24px;
}

@media (max-width: 640px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.profile-field-box {
  background: var(--bg-page);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 18px;
}

body.dark-mode .profile-field-box {
  background: #0f172a;
  border-color: #1e293b;
}

.profile-field-label {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--ink-faint);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.profile-field-val {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--ink);
  word-break: break-all;
}

.profile-section-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.profile-btn-logout {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  background: transparent;
  border: 1px solid #ef4444;
  color: #ef4444;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.profile-btn-logout:hover {
  background: #ef4444;
  color: #ffffff;
}

.profile-empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--line-subtle);
  color: var(--ink-muted);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

body.dark-mode .empty-icon-circle {
  background: #1e293b;
  color: #94a3b8;
}

.profile-empty-state h3 {
  font-size: 20px;
  font-weight: 800;
  color: var(--ink);
  margin-bottom: 8px;
}

.profile-empty-state p {
  font-size: 14px;
  color: var(--ink-muted);
  max-width: 420px;
  margin: 0 auto 20px;
}
"""

def render_profile_view() -> str:
    """Renders the Removix Account Profile page."""
    main_html = """
    <div class="profile-container">
      <!-- 1. Logged In Profile Card (Hidden if logged out) -->
      <div id="profileLoggedInView" style="display:none;">
        <div class="profile-card">
          <div class="profile-header-row">
            <div class="profile-avatar-large" id="profilePageAvatar">U</div>
            <div class="profile-title-group">
              <h2 id="profilePageEmail">—</h2>
              <div class="profile-badges-row">
                <span class="profile-badge badge-active">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>
                  Active Account
                </span>
                <span class="profile-badge badge-supabase">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                  Supabase Auth
                </span>
              </div>
            </div>
          </div>

          <!-- Profile Fields Grid -->
          <div class="profile-grid">
            <div class="profile-field-box">
              <div class="profile-field-label">Email Address</div>
              <div class="profile-field-val" id="profileFieldEmail">—</div>
            </div>
            <div class="profile-field-box">
              <div class="profile-field-label">User ID</div>
              <div class="profile-field-val" id="profileFieldId" style="font-family:monospace; font-size:12.5px;">—</div>
            </div>
            <div class="profile-field-box">
              <div class="profile-field-label">Auth Provider</div>
              <div class="profile-field-val" id="profileFieldProvider">Email / Password</div>
            </div>
            <div class="profile-field-box">
              <div class="profile-field-label">Current Plan</div>
              <div class="profile-field-val" style="color:var(--primary); font-weight:700;">Removix Free Tier</div>
            </div>
          </div>

          <div style="margin-top:28px; display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--line); padding-top:20px;">
            <p style="font-size:13px; color:var(--ink-muted); margin:0;">Full profile customization and cloud storage dashboard coming in next update.</p>
            <button type="button" class="profile-btn-logout" onclick="handleSupabaseSignOut()">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              Logout
            </button>
          </div>
        </div>
      </div>

      <!-- 2. Logged Out View (Shown when not authenticated) -->
      <div id="profileLoggedOutView">
        <div class="profile-card profile-empty-state">
          <div class="empty-icon-circle">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <h3>Account Authentication Required</h3>
          <p>Please log in or create a Removix account using Supabase Auth to view your profile details and settings.</p>
          <button type="button" class="btn-nav-login" onclick="openLoginModal()" style="font-size:14px; padding:10px 24px;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            Sign In / Create Account
          </button>
        </div>
      </div>
    </div>
    """

    profile_js = """
    function syncProfilePageUI(session) {
      var loggedInView = document.getElementById('profileLoggedInView');
      var loggedOutView = document.getElementById('profileLoggedOutView');
      if (!loggedInView || !loggedOutView) return;

      if (session && session.user) {
        loggedInView.style.display = 'block';
        loggedOutView.style.display = 'none';

        var email = session.user.email || 'User';
        var initial = email.charAt(0).toUpperCase();
        var provider = (session.user.app_metadata && session.user.app_metadata.provider) || 'Email';

        document.getElementById('profilePageEmail').textContent = email;
        document.getElementById('profilePageAvatar').textContent = initial;
        document.getElementById('profileFieldEmail').textContent = email;
        document.getElementById('profileFieldId').textContent = session.user.id || '—';
        document.getElementById('profileFieldProvider').textContent = provider.charAt(0).toUpperCase() + provider.slice(1);
      } else {
        loggedInView.style.display = 'none';
        loggedOutView.style.display = 'block';
      }
    }

    document.addEventListener('removix:auth-changed', function(e) {
      syncProfilePageUI(e.detail ? e.detail.session : null);
    });

    document.addEventListener('DOMContentLoaded', function() {
      if (window.removixGetSession) {
        syncProfilePageUI(window.removixGetSession());
      }
    });
    """

    return render_layout(
        title="Account Profile",
        active_tool="",
        hero_title="Account Profile",
        hero_sub="View and manage your Removix profile and Supabase authentication session.",
        main_card_html=main_html,
        feature_cards_html="",
        extra_css=PROFILE_CSS,
        extra_js=profile_js,
    )
