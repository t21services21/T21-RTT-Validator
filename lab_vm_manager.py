"""
LAB VM MANAGER
Manage virtual machines for hands-on labs

Features:
- VM provisioning
- Lab environment setup
- Student access management
- Resource monitoring
- Automatic cleanup
"""

import hashlib
import random
from datetime import datetime, timedelta

class LabVMManager:
    """
    Virtual Machine Manager for Cyber Labs
    In production: Integrate with AWS, Azure, or DigitalOcean
    """
    
    def __init__(self):
        self.active_vms = {}
        self.vm_templates = self.initialize_templates()
    
    def initialize_templates(self):
        """Initialize VM templates for different labs"""
        
        return {
            "linux_basics": {
                "name": "Ubuntu 22.04 Basic",
                "os": "Ubuntu 22.04",
                "cpu": 1,
                "ram": 1024,
                "disk": 10,
                "software": ["bash", "vim", "basic-tools"],
                "setup_time": 60  # seconds
            },
            "linux_privilege_escalation": {
                "name": "Ubuntu 22.04 Vulnerable",
                "os": "Ubuntu 22.04",
                "cpu": 2,
                "ram": 2048,
                "disk": 20,
                "software": ["bash", "vim", "suid-binaries", "vulnerable-services"],
                "setup_time": 120
            },
            "network_scanning": {
                "name": "Network Lab",
                "os": "Kali Linux",
                "cpu": 2,
                "ram": 4096,
                "disk": 30,
                "software": ["nmap", "wireshark", "metasploit"],
                "setup_time": 180
            },
            "web_hacking": {
                "name": "DVWA + Kali",
                "os": "Multi-VM",
                "cpu": 4,
                "ram": 8192,
                "disk": 40,
                "software": ["dvwa", "kali-tools", "burp-suite"],
                "setup_time": 240
            },
            "malware_analysis": {
                "name": "Malware Analysis Lab",
                "os": "Windows 10 + REMnux",
                "cpu": 4,
                "ram": 8192,
                "disk": 50,
                "software": ["ida-free", "ghidra", "cuckoo", "volatility"],
                "setup_time": 300
            },
            "forensics": {
                "name": "Digital Forensics Lab",
                "os": "Ubuntu 22.04",
                "cpu": 4,
                "ram": 8192,
                "disk": 100,
                "software": ["autopsy", "volatility", "ftk-imager", "wireshark"],
                "setup_time": 240
            }
        }
    
    def provision_vm(self, student_id, lab_type, lab_id):
        """
        Provision a new VM for student
        In production: Call cloud provider API
        """
        
        if lab_type not in self.vm_templates:
            return None
        
        template = self.vm_templates[lab_type]
        
        # Generate unique VM ID
        vm_id = hashlib.sha256(
            f"{student_id}{lab_id}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        # Generate access credentials
        vm_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        ssh_port = random.randint(2222, 9999)
        password = self.generate_password()
        
        # Create VM record
        vm = {
            "vm_id": vm_id,
            "student_id": student_id,
            "lab_id": lab_id,
            "lab_type": lab_type,
            "template": template,
            "status": "provisioning",
            "ip_address": vm_ip,
            "ssh_port": ssh_port,
            "username": "student",
            "password": password,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=4),
            "access_url": f"https://lab.t21services.co.uk/{vm_id}"
        }
        
        self.active_vms[vm_id] = vm
        
        # In production: Actually provision VM via cloud API
        # For now: Simulate provisioning
        vm['status'] = 'running'
        
        return vm
    
    def generate_password(self):
        """Generate secure random password"""
        import string
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(12))
    
    def get_vm_status(self, vm_id):
        """Get VM status"""
        
        if vm_id not in self.active_vms:
            return None
        
        vm = self.active_vms[vm_id]
        
        # Check if expired
        if datetime.now() > vm['expires_at']:
            vm['status'] = 'expired'
            self.cleanup_vm(vm_id)
        
        return vm
    
    def extend_vm_time(self, vm_id, hours=2):
        """Extend VM runtime"""
        
        if vm_id in self.active_vms:
            self.active_vms[vm_id]['expires_at'] += timedelta(hours=hours)
            return True
        return False
    
    def reset_vm(self, vm_id):
        """Reset VM to initial state"""
        
        if vm_id in self.active_vms:
            vm = self.active_vms[vm_id]
            vm['status'] = 'resetting'
            
            # In production: Call cloud API to reset
            vm['status'] = 'running'
            return True
        return False
    
    def cleanup_vm(self, vm_id):
        """Cleanup and destroy VM"""
        
        if vm_id in self.active_vms:
            vm = self.active_vms[vm_id]
            vm['status'] = 'destroying'
            
            # In production: Call cloud API to destroy
            del self.active_vms[vm_id]
            return True
        return False
    
    def get_student_vms(self, student_id):
        """Get all VMs for a student"""
        
        return [
            vm for vm in self.active_vms.values()
            if vm['student_id'] == student_id
        ]
    
    def cleanup_expired_vms(self):
        """Cleanup all expired VMs"""
        
        now = datetime.now()
        expired = [
            vm_id for vm_id, vm in self.active_vms.items()
            if now > vm['expires_at']
        ]
        
        for vm_id in expired:
            self.cleanup_vm(vm_id)
        
        return len(expired)
    
    def get_resource_usage(self):
        """Get current resource usage"""
        
        total_cpu = sum(vm['template']['cpu'] for vm in self.active_vms.values())
        total_ram = sum(vm['template']['ram'] for vm in self.active_vms.values())
        total_disk = sum(vm['template']['disk'] for vm in self.active_vms.values())
        
        return {
            "active_vms": len(self.active_vms),
            "total_cpu_cores": total_cpu,
            "total_ram_mb": total_ram,
            "total_disk_gb": total_disk
        }

# VM Manager instance
vm_manager = LabVMManager()

# Streamlit UI for lab access
def render_lab_interface(student_id, lab_id, lab_type):
    """Render lab interface for student"""
    
    import streamlit as st
    
    # Check if VM already exists
    student_vms = vm_manager.get_student_vms(student_id)
    active_vm = next((vm for vm in student_vms if vm['lab_id'] == lab_id), None)
    
    if not active_vm:
        # Provision new VM
        st.info("🚀 Launching lab environment...")
        
        with st.spinner("Setting up your virtual machine..."):
            import time
            time.sleep(2)  # Simulate setup
            
            active_vm = vm_manager.provision_vm(student_id, lab_type, lab_id)
        
        if active_vm:
            st.success("✅ Lab environment ready!")
            st.balloons()
    
    if active_vm:
        # Display VM info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🖥️ Lab Environment")
            st.markdown(f"**Status:** 🟢 {active_vm['status'].title()}")
            st.markdown(f"**Template:** {active_vm['template']['name']}")
            st.markdown(f"**OS:** {active_vm['template']['os']}")
            
        with col2:
            st.markdown("### ⏱️ Session Info")
            time_remaining = active_vm['expires_at'] - datetime.now()
            hours = int(time_remaining.total_seconds() / 3600)
            minutes = int((time_remaining.total_seconds() % 3600) / 60)
            st.markdown(f"**Time Remaining:** {hours}h {minutes}m")
            
            if st.button("⏰ Extend Time (+2h)"):
                vm_manager.extend_vm_time(active_vm['vm_id'], 2)
                st.success("Time extended!")
                st.rerun()
        
        st.markdown("---")
        
        # Access methods
        st.markdown("### 🔗 Access Your Lab")
        
        tab1, tab2, tab3 = st.tabs(["🌐 Web Terminal", "💻 SSH Access", "📋 Credentials"])
        
        with tab1:
            st.markdown("**Browser-based terminal:**")
            st.markdown(f"[🚀 Open Web Terminal]({active_vm['access_url']})")
            
            # Embed terminal (in production)
            st.info("Terminal will open in new window")
        
        with tab2:
            st.markdown("**SSH Connection:**")
            st.code(f"ssh {active_vm['username']}@{active_vm['ip_address']} -p {active_vm['ssh_port']}")
            st.markdown(f"**Password:** `{active_vm['password']}`")
        
        with tab3:
            st.markdown("**Lab Credentials:**")
            st.markdown(f"**Username:** {active_vm['username']}")
            st.markdown(f"**Password:** {active_vm['password']}")
            st.markdown(f"**IP Address:** {active_vm['ip_address']}")
            st.markdown(f"**SSH Port:** {active_vm['ssh_port']}")
        
        st.markdown("---")
        
        # Lab controls
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        
        with col_ctrl1:
            if st.button("🔄 Reset Lab", use_container_width=True):
                vm_manager.reset_vm(active_vm['vm_id'])
                st.success("Lab reset!")
                st.rerun()
        
        with col_ctrl2:
            if st.button("💾 Save Progress", use_container_width=True):
                st.info("Progress saved!")
        
        with col_ctrl3:
            if st.button("❌ End Session", use_container_width=True):
                vm_manager.cleanup_vm(active_vm['vm_id'])
                st.success("Session ended!")
                st.rerun()
        
        return active_vm
    
    return None
