"""
Success Message Utilities
Enhanced success messages for better user experience across all modules
"""
import streamlit as st


def show_success_with_balloons(title: str, message: str, details: dict = None, next_steps: str = None):
    """
    Display enhanced success message with balloons
    
    Args:
        title: Main success title (e.g., "PATHWAY CREATED SUCCESSFULLY!")
        message: Main success message
        details: Optional dict of key-value pairs to display
        next_steps: Optional next steps message
    """
    st.balloons()
    
    success_text = f"✅ **{title}**\n\n{message}\n\n"
    
    if details:
        for key, value in details.items():
            success_text += f"**{key}:** {value}  \n"
        success_text += "\n"
    
    success_text += "✔️ **Operation completed successfully!**"
    
    st.success(success_text)
    
    if next_steps:
        st.info(f"💡 **Next Steps:** {next_steps}")


def show_simple_success(message: str, include_balloons: bool = True):
    """
    Display simple success message with optional balloons
    
    Args:
        message: Success message to display
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    st.success(f"""
    ✅ **SUCCESS!**
    
    {message}
    
    ✔️ Operation completed!
    """)


def show_data_saved_success(entity_name: str, entity_id: str = None, include_balloons: bool = True):
    """
    Display success message for data saving operations
    
    Args:
        entity_name: Name of entity saved (e.g., "Patient", "Pathway", "Episode")
        entity_id: Optional ID of saved entity
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    message = f"✅ **{entity_name.upper()} SAVED SUCCESSFULLY!**\n\n"
    
    if entity_id:
        message += f"**ID:** {entity_id}  \n"
    
    message += f"✔️ {entity_name} has been saved to the database!  \n"
    message += "📊 All data has been recorded permanently!"
    
    st.success(message)


def show_update_success(entity_name: str, what_changed: str = None, include_balloons: bool = True):
    """
    Display success message for update operations
    
    Args:
        entity_name: Name of entity updated (e.g., "Patient Record", "Pathway Status")
        what_changed: Optional description of what changed
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    message = f"✅ **{entity_name.upper()} UPDATED SUCCESSFULLY!**\n\n"
    
    if what_changed:
        message += f"{what_changed}  \n\n"
    
    message += f"✔️ {entity_name} has been updated!  \n"
    message += "💾 Changes have been saved!"
    
    st.success(message)


def show_deletion_success(entity_name: str, include_balloons: bool = False):
    """
    Display success message for deletion operations
    
    Args:
        entity_name: Name of entity deleted
        include_balloons: Whether to show balloons animation (usually False for deletions)
    """
    if include_balloons:
        st.balloons()
    
    st.success(f"""
    ✅ **{entity_name.upper()} DELETED SUCCESSFULLY!**
    
    🗑️ {entity_name} has been removed from the system  
    ✔️ Deletion completed!
    """)


def show_task_completed_success(task_name: str, result_details: str = None, include_balloons: bool = True):
    """
    Display success message for task completion
    
    Args:
        task_name: Name of completed task
        result_details: Optional details about results
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    message = f"✅ **{task_name.upper()} COMPLETED SUCCESSFULLY!**\n\n"
    
    if result_details:
        message += f"{result_details}  \n\n"
    
    message += f"✔️ Task has been completed!  \n"
    message += "📋 All actions have been processed!"
    
    st.success(message)


def show_email_sent_success(recipient_count: int = None, include_balloons: bool = True):
    """
    Display success message for email sending
    
    Args:
        recipient_count: Optional number of recipients
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    message = "✅ **EMAIL SENT SUCCESSFULLY!**\n\n"
    
    if recipient_count:
        message += f"📧 Sent to {recipient_count} recipient(s)  \n"
    
    message += "✔️ Email has been delivered!  \n"
    message += "📮 Message is on its way!"
    
    st.success(message)


def show_approval_success(what_approved: str, include_balloons: bool = True):
    """
    Display success message for approval operations
    
    Args:
        what_approved: What was approved
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    st.success(f"""
    ✅ **APPROVED SUCCESSFULLY!**
    
    ✔️ {what_approved} has been approved  
    📋 Approval recorded in the system  
    
    **Status:** Approval complete!
    """)


def show_rejection_success(what_rejected: str, include_balloons: bool = False):
    """
    Display success message for rejection operations
    
    Args:
        what_rejected: What was rejected
        include_balloons: Whether to show balloons animation (usually False for rejections)
    """
    if include_balloons:
        st.balloons()
    
    st.warning(f"""
    ✅ **REJECTION RECORDED SUCCESSFULLY!**
    
    ❌ {what_rejected} has been rejected  
    📋 Rejection recorded in the system  
    
    **Status:** Rejection complete!
    """)


def show_upload_success(file_count: int = 1, file_type: str = "file", include_balloons: bool = True):
    """
    Display success message for file upload operations
    
    Args:
        file_count: Number of files uploaded
        file_type: Type of file(s) uploaded
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    if file_count == 1:
        message = f"✅ **{file_type.upper()} UPLOADED SUCCESSFULLY!**\n\n"
    else:
        message = f"✅ **{file_count} {file_type.upper()}S UPLOADED SUCCESSFULLY!**\n\n"
    
    message += f"📁 File(s) have been uploaded  \n"
    message += "✔️ Upload complete!"
    
    st.success(message)


def show_export_success(what_exported: str, include_balloons: bool = True):
    """
    Display success message for export operations
    
    Args:
        what_exported: What was exported
        include_balloons: Whether to show balloons animation
    """
    if include_balloons:
        st.balloons()
    
    st.success(f"""
    ✅ **EXPORT COMPLETED SUCCESSFULLY!**
    
    📊 {what_exported} has been exported  
    💾 Download is ready!  
    
    ✔️ Export complete!
    """)


# Example usage templates for documentation
USAGE_EXAMPLES = """
# Usage Examples:

## 1. Pathway Created
from success_messages import show_success_with_balloons
show_success_with_balloons(
    title="PATHWAY CREATED SUCCESSFULLY!",
    message="RTT Clock Started ⏱️",
    details={
        "Pathway ID": "P12345",
        "Breach Date": "01/04/2026",
        "Status": "Active"
    },
    next_steps="You can now manage this pathway, record milestones, or pause/resume the clock."
)

## 2. Simple Success
from success_messages import show_simple_success
show_simple_success("Patient record has been updated with new information!")

## 3. Data Saved
from success_messages import show_data_saved_success
show_data_saved_success("Patient", entity_id="PT123456")

## 4. Update Success
from success_messages import show_update_success
show_update_success("Pathway Status", what_changed="Status changed from 'Active' to 'Paused'")

## 5. Email Sent
from success_messages import show_email_sent_success
show_email_sent_success(recipient_count=5)
"""
