import hashlib
import json
import subprocess
import sys
import os

def generate_hash(pan_path, user_id):
    """Generate SHA-256 hashes for the PAN image and User ID"""
    with open(pan_path, "rb") as f:
        pan_hash = hashlib.sha256(f.read()).hexdigest()

    user_hash = hashlib.sha256(user_id.encode()).hexdigest()
    combined_hash = hashlib.sha256((pan_hash + user_hash).encode()).hexdigest()

    return pan_hash, user_hash, combined_hash

def save_input_json(pan_hash, user_hash):
    """Save PAN and User ID hashes in input.json"""
    data = {
        "pan_hash": int(pan_hash, 16),
        "user_id": int(user_hash, 16)
    }

    with open("input.json", "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Hashes generated and saved to input.json")

def run_command(command):
    """Run a shell command and handle errors"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}\n{e}")
        sys.exit(1)

def automate_process(pan_path, user_id):
    """Full automation of ZKP and Blockchain Deployment"""
    
    # Step 1: Generate hashes and save input.json
    print("\n🔹 Generating hashes...")
    pan_hash, user_hash, _ = generate_hash(pan_path, user_id)
    save_input_json(pan_hash, user_hash)

    # Step 2: Run witness generation
    print("\n🔹 Generating witness.wtns...")
    run_command("node PANProof_js/generate_witness.js PANProof_js/PANProof.wasm input.json witness.wtns")

    # Step 3: Generate proof.json and public.json
    print("\n🔹 Generating proof.json and public.json...")
    run_command("npx snarkjs groth16 prove circuit_final.zkey witness.wtns proof.json public.json")
    #run_command("snarkjs groth16 prove circuit_final.zkey witness.wtns proof.json public.json")

    print("\n✅ ZKP proof successfully generated!")

    # Step 4: Deploy Smart Contract on Blockchain using 'cd blockchain-storage'
    print("\n🔹 Deploying Smart Contract on Blockchain...")

    blockchain_dir = "blockchain-storage"
    deploy_script_path = os.path.join(blockchain_dir, "scripts/deploy.js")

    if not os.path.exists(deploy_script_path):
        print("❌ Error: The deployment script 'deploy.js' was not found in blockchain-storage.")
        sys.exit(1)

    # ✅ Only this step uses `cd blockchain-storage && ...`
    run_command(f"cd {blockchain_dir} && npx hardhat run scripts/deploy.js --network localhost")

    print("\n🚀 Smart Contract Successfully Deployed!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 automate_zkp.py <pan_image_path> <user_id>")
        sys.exit(1)

    pan_image_path = sys.argv[1]
    user_id = sys.argv[2]

    automate_process(pan_image_path, user_id)
