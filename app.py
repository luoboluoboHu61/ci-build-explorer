import streamlit as st
from github_api import get_workflow_runs
from db import init_db, insert_builds, fetch_all_builds
from datetime import datetime
from datetime import date

def format_time(time_str):
    if not time_str:
        return "—"
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def fake_log_for_failure(build_id):
    return f"""
[Error] Build #{build_id} failed due to flaky test failure.
[StackTrace] AssertionError: expected X but got Y
File "/app/src/module.py", line 42, in critical_function
"""

def main():
    st.title("🚧 CI Build Explorer")

    # 初始化数据库
    init_db()

    # 拉取最新构建按钮
    if st.button("🔄 Sync Latest Builds"):
        builds = get_workflow_runs()
        insert_builds(builds)
        st.success("✅ Synced from GitHub!")

    # 获取本地构建数据
    builds = fetch_all_builds()

    if not builds:
        st.warning("No builds found.")
        return

    st.subheader("🔍 Search & Filter")

    # Step 4.1 - 搜索 & 时间筛选
    search_id = st.text_input("🔎 Enter Build ID")
    today = date.today()
    start_date = st.date_input("📅 Start Date", value=today.replace(day=1))
    end_date = st.date_input("📅 End Date", value=today)

    # 时间筛选逻辑
    def is_within_range(build):
        if not build['start_time']:
            return False
        dt = datetime.strptime(build['start_time'], "%Y-%m-%dT%H:%M:%SZ").date()
        return start_date <= dt <= end_date

    # 搜索筛选逻辑
    filtered_builds = [
        b for b in builds
        if (search_id == "" or str(b['id']) == search_id)
        and is_within_range(b)
    ]

    st.write(f"Showing {len(filtered_builds)} builds.")

    st.subheader("📋 Build History")
 
    for build in filtered_builds:
        # Normalize conclusion string
        conclusion = (build['conclusion'] or 'in_progress').strip().lower()
        status_icon = "❌" if conclusion == "failure" else "✅"
        color = "red" if conclusion == "failure" else "green"

        with st.expander(f"{status_icon} Build #{build['id']} – {build['branch']} – :{color}[{conclusion}]"):
            st.write(f"🧠 Commit: {build['commit_msg']}")
            st.write(f"🔁 Status: `{build['status']}`")
            st.write(f"✅ Result: `{conclusion}`")
            st.write(f"🕒 Start Time: {format_time(build['start_time'])}")
            st.write(f"🕓 End Time: {format_time(build['end_time'])}")

            if conclusion == "failure":
                st.error("❌ Build failed. Showing mock logs below:")
                st.code(fake_log_for_failure(build['id']), language='bash')
                st.info("🔁 Simulate Replay: You can now re-run this build manually.")



if __name__ == "__main__":
    main()
