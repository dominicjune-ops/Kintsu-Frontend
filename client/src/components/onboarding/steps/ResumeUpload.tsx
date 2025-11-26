import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Upload, FileText, CheckCircle2, Loader2 } from "lucide-react";

interface ResumeUploadProps {
  file: File | null;
  onFileSelect: (file: File) => void;
}

export function ResumeUpload({ file, onFileSelect }: ResumeUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isScanning, setIsScanning] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile && isValidFileType(droppedFile)) {
        simulateScan(droppedFile);
      }
    },
    [onFileSelect]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile && isValidFileType(selectedFile)) {
        simulateScan(selectedFile);
      }
    },
    [onFileSelect]
  );

  const simulateScan = (file: File) => {
    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
      onFileSelect(file);
    }, 2000);
  };

  const isValidFileType = (file: File) => {
    const validTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];
    return validTypes.includes(file.type);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="text-center space-y-3">
        <h2 className="text-3xl md:text-4xl font-bold font-serif bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          Upload your resume
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          We'll analyze it and help you craft the perfect application for every opportunity
        </p>
      </div>

      {/* Upload Area */}
      <div className="max-w-2xl mx-auto">
        <Card
          className={`relative overflow-hidden transition-all duration-300 ${
            isDragging
              ? "ring-2 ring-accent shadow-xl shadow-accent/20 scale-[1.02]"
              : ""
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="p-12">
            <AnimatePresence mode="wait">
              {isScanning ? (
                <ScanningAnimation key="scanning" />
              ) : file ? (
                <UploadedFile key="uploaded" file={file} />
              ) : (
                <UploadPrompt key="prompt" onFileInput={handleFileInput} />
              )}
            </AnimatePresence>
          </div>
        </Card>

        {/* File Type Info */}
        <p className="text-center text-sm text-muted-foreground mt-4">
          Supported formats: PDF, DOC, DOCX • Max size: 10MB
        </p>
      </div>
    </motion.div>
  );
}

function UploadPrompt({ onFileInput }: { onFileInput: (e: React.ChangeEvent<HTMLInputElement>) => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="text-center space-y-6"
    >
      <motion.div
        animate={{
          y: [0, -10, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-accent/10"
      >
        <Upload className="h-10 w-10 text-accent" />
      </motion.div>

      <div className="space-y-2">
        <h3 className="text-xl font-semibold">Drop your resume here</h3>
        <p className="text-muted-foreground">or click to browse files</p>
      </div>

      <input
        type="file"
        id="resume-upload"
        className="hidden"
        accept=".pdf,.doc,.docx"
        onChange={onFileInput}
      />
      <label
        htmlFor="resume-upload"
        className="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-accent text-accent-foreground font-medium cursor-pointer hover:bg-accent/90 transition-colors"
      >
        Browse Files
      </label>
    </motion.div>
  );
}

function ScanningAnimation() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="text-center space-y-6"
    >
      <div className="relative inline-flex items-center justify-center w-20 h-20">
        <motion.div
          className="absolute inset-0 rounded-full border-4 border-accent/20"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.5, 0, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <Loader2 className="h-10 w-10 text-accent animate-spin" />
      </div>

      <div className="space-y-2">
        <h3 className="text-xl font-semibold">Scanning your resume...</h3>
        <p className="text-muted-foreground">Analyzing your experience and skills</p>
      </div>

      {/* Scanning Progress */}
      <div className="space-y-3 max-w-xs mx-auto">
        {["Reading content", "Identifying skills", "Analyzing experience"].map((text, index) => (
          <motion.div
            key={text}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.3 }}
            className="flex items-center gap-2 text-sm text-muted-foreground"
          >
            <motion.div
              className="h-2 w-2 rounded-full bg-accent"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                delay: index * 0.3
              }}
            />
            {text}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

function UploadedFile({ file }: { file: File }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="text-center space-y-6"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 200, damping: 15 }}
        className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-500/10"
      >
        <CheckCircle2 className="h-10 w-10 text-green-500" />
      </motion.div>

      <div className="space-y-3">
        <h3 className="text-xl font-semibold">Resume uploaded successfully!</h3>

        <div className="inline-flex items-center gap-3 px-4 py-3 rounded-lg bg-muted">
          <FileText className="h-5 w-5 text-muted-foreground" />
          <div className="text-left">
            <p className="text-sm font-medium">{file.name}</p>
            <p className="text-xs text-muted-foreground">
              {formatFileSize(file.size)}
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function formatFileSize(bytes: number) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
}
