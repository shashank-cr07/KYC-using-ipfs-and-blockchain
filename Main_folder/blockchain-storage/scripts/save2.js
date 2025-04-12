const fs = require("fs");
const path = require("path");
const { ethers } = require("hardhat");

async function main() {
    try {
        // Get contract address from environment variable
        const contractAddress = process.env.CONTRACT_ADDRESS;

        if (!contractAddress) {
            throw new Error("❌ Contract address is required! Run: CONTRACT_ADDRESS=<contract_address> npx hardhat run save2.js --network localhost");
        }

        // Get contract instance
        const contract = await ethers.getContractAt("ZKPStorage", contractAddress);

        // Query blockchain for stored data
        const data = await contract.getBlockData(1);

        // Remove surrounding single quotes if present
        const cleanData = data.map(str => str.trim().replace(/^'|'$/g, ""));

        // Define file paths
        const verificationKeyPath = path.resolve(__dirname, "../verifyJSON/verification_key.json");
        const publicDataPath = path.resolve(__dirname, "../verifyJSON/public.json");
        const proofPath = path.resolve(__dirname, "../verifyJSON/proof.json");

        // Save data to JSON files
        fs.writeFileSync(verificationKeyPath, cleanData[0], "utf8");
        fs.writeFileSync(publicDataPath, cleanData[1], "utf8");
        fs.writeFileSync(proofPath, cleanData[2], "utf8");

        console.log("✅ Data successfully retrieved and saved!");
    } catch (error) {
        console.error("❌ Error:", error.message);
        process.exit(1);
    }
}

main();
