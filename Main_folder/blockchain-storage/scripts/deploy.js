const fs = require("fs");
const path = require("path");
const { ethers } = require("hardhat");

async function main() {
    try {
        // Resolve absolute paths
        const verificationKey = `'${fs.readFileSync(path.resolve(__dirname, "../../verification_key.json"), "utf8").trim()}'`;
        const publicData = `'${fs.readFileSync(path.resolve(__dirname, "../../public.json"), "utf8").trim()}'`;
        const proof = `'${fs.readFileSync(path.resolve(__dirname, "../../proof.json"), "utf8").trim()}'`;

        console.log("✅ JSON Files Loaded Successfully!");
        
        // Deploy contract
        const ZKPStorage = await ethers.getContractFactory("ZKPStorage");
        const contract = await ZKPStorage.deploy(verificationKey, publicData, proof);

        // Use `waitForDeployment()` instead of `deployed()`
        await contract.waitForDeployment();

        console.log("🚀 Contract deployed at:", await contract.getAddress());
    } catch (error) {
        console.error("❌ Error:", error.message);
        process.exit(1);
    }
}

main();
