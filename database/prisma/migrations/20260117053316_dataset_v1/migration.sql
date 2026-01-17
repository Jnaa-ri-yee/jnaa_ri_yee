-- CreateEnum
CREATE TYPE "SampleType" AS ENUM ('IMAGE', 'VIDEO');

-- CreateEnum
CREATE TYPE "BoxLabel" AS ENUM ('HAND', 'BODY', 'FACE', 'OBJECT');

-- CreateEnum
CREATE TYPE "KeypointType" AS ENUM ('HAND', 'BODY', 'FACE');

-- CreateEnum
CREATE TYPE "Difficulty" AS ENUM ('BASIC', 'INTERMEDIATE', 'ADVANCED');

-- CreateEnum
CREATE TYPE "Quality" AS ENUM ('PENDING', 'LOW', 'MEDIUM', 'HIGH', 'EXCELLENT');

-- CreateEnum
CREATE TYPE "DataSource" AS ENUM ('MANUAL', 'BATCH', 'GENERATED', 'EXTERNAL');

-- CreateEnum
CREATE TYPE "TagType" AS ENUM ('GENERAL', 'LINGUISTIC', 'TECHNICAL', 'DIFFICULTY');

-- CreateEnum
CREATE TYPE "BatchStatus" AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED');

-- CreateTable
CREATE TABLE "Category" (
    "id" SERIAL NOT NULL,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "order" INTEGER NOT NULL DEFAULT 0,
    "parentId" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Category_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Sign" (
    "id" SERIAL NOT NULL,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "difficulty" "Difficulty" NOT NULL DEFAULT 'BASIC',
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "categoryId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Sign_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Tag" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "type" "TagType" NOT NULL DEFAULT 'GENERAL',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Tag_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SignTag" (
    "signId" INTEGER NOT NULL,
    "tagId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "SignTag_pkey" PRIMARY KEY ("signId","tagId")
);

-- CreateTable
CREATE TABLE "Sample" (
    "id" SERIAL NOT NULL,
    "type" "SampleType" NOT NULL,
    "filePath" TEXT NOT NULL,
    "originalName" TEXT,
    "fileSize" INTEGER,
    "width" INTEGER,
    "height" INTEGER,
    "fps" INTEGER,
    "duration" DOUBLE PRECISION,
    "format" TEXT,
    "quality" "Quality" NOT NULL DEFAULT 'PENDING',
    "isValidated" BOOLEAN NOT NULL DEFAULT false,
    "validatedBy" TEXT,
    "validatedAt" TIMESTAMP(3),
    "source" "DataSource" NOT NULL DEFAULT 'MANUAL',
    "uploadBatchId" TEXT,
    "signId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Sample_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "BoundingBox" (
    "id" SERIAL NOT NULL,
    "x" DOUBLE PRECISION NOT NULL,
    "y" DOUBLE PRECISION NOT NULL,
    "width" DOUBLE PRECISION NOT NULL,
    "height" DOUBLE PRECISION NOT NULL,
    "label" "BoxLabel" NOT NULL,
    "confidence" DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    "sampleId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "BoundingBox_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "KeypointSet" (
    "id" SERIAL NOT NULL,
    "type" "KeypointType" NOT NULL,
    "data" JSONB NOT NULL,
    "confidence" DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    "sampleId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "KeypointSet_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SampleMeta" (
    "id" SERIAL NOT NULL,
    "key" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "sampleId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "SampleMeta_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "UploadBatch" (
    "id" TEXT NOT NULL,
    "name" TEXT,
    "description" TEXT,
    "totalFiles" INTEGER NOT NULL DEFAULT 0,
    "processed" INTEGER NOT NULL DEFAULT 0,
    "successful" INTEGER NOT NULL DEFAULT 0,
    "failed" INTEGER NOT NULL DEFAULT 0,
    "status" "BatchStatus" NOT NULL DEFAULT 'PENDING',
    "targetCategoryId" INTEGER,
    "autoValidate" BOOLEAN NOT NULL DEFAULT false,
    "errors" TEXT,
    "startedAt" TIMESTAMP(3),
    "completedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "UploadBatch_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Category_code_key" ON "Category"("code");

-- CreateIndex
CREATE INDEX "Category_parentId_idx" ON "Category"("parentId");

-- CreateIndex
CREATE INDEX "Category_code_idx" ON "Category"("code");

-- CreateIndex
CREATE UNIQUE INDEX "Sign_code_key" ON "Sign"("code");

-- CreateIndex
CREATE INDEX "Sign_categoryId_idx" ON "Sign"("categoryId");

-- CreateIndex
CREATE INDEX "Sign_code_idx" ON "Sign"("code");

-- CreateIndex
CREATE INDEX "Sign_difficulty_idx" ON "Sign"("difficulty");

-- CreateIndex
CREATE UNIQUE INDEX "Tag_name_key" ON "Tag"("name");

-- CreateIndex
CREATE INDEX "Sample_signId_type_idx" ON "Sample"("signId", "type");

-- CreateIndex
CREATE INDEX "Sample_quality_idx" ON "Sample"("quality");

-- CreateIndex
CREATE INDEX "Sample_uploadBatchId_idx" ON "Sample"("uploadBatchId");

-- CreateIndex
CREATE INDEX "Sample_createdAt_idx" ON "Sample"("createdAt");

-- CreateIndex
CREATE INDEX "Sample_signId_quality_type_idx" ON "Sample"("signId", "quality", "type");

-- CreateIndex
CREATE INDEX "BoundingBox_sampleId_idx" ON "BoundingBox"("sampleId");

-- CreateIndex
CREATE INDEX "KeypointSet_sampleId_type_idx" ON "KeypointSet"("sampleId", "type");

-- CreateIndex
CREATE INDEX "SampleMeta_sampleId_key_idx" ON "SampleMeta"("sampleId", "key");

-- CreateIndex
CREATE INDEX "UploadBatch_status_idx" ON "UploadBatch"("status");

-- CreateIndex
CREATE INDEX "UploadBatch_createdAt_idx" ON "UploadBatch"("createdAt");

-- AddForeignKey
ALTER TABLE "Category" ADD CONSTRAINT "Category_parentId_fkey" FOREIGN KEY ("parentId") REFERENCES "Category"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sign" ADD CONSTRAINT "Sign_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SignTag" ADD CONSTRAINT "SignTag_signId_fkey" FOREIGN KEY ("signId") REFERENCES "Sign"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SignTag" ADD CONSTRAINT "SignTag_tagId_fkey" FOREIGN KEY ("tagId") REFERENCES "Tag"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sample" ADD CONSTRAINT "Sample_uploadBatchId_fkey" FOREIGN KEY ("uploadBatchId") REFERENCES "UploadBatch"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sample" ADD CONSTRAINT "Sample_signId_fkey" FOREIGN KEY ("signId") REFERENCES "Sign"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "BoundingBox" ADD CONSTRAINT "BoundingBox_sampleId_fkey" FOREIGN KEY ("sampleId") REFERENCES "Sample"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "KeypointSet" ADD CONSTRAINT "KeypointSet_sampleId_fkey" FOREIGN KEY ("sampleId") REFERENCES "Sample"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SampleMeta" ADD CONSTRAINT "SampleMeta_sampleId_fkey" FOREIGN KEY ("sampleId") REFERENCES "Sample"("id") ON DELETE CASCADE ON UPDATE CASCADE;
