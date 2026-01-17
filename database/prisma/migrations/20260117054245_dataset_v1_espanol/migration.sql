/*
  Warnings:

  - You are about to drop the `BoundingBox` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Category` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `KeypointSet` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Sample` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `SampleMeta` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Sign` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `SignTag` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Tag` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `UploadBatch` table. If the table is not empty, all the data it contains will be lost.

*/
-- CreateEnum
CREATE TYPE "TipoMuestra" AS ENUM ('IMAGEN', 'VIDEO');

-- CreateEnum
CREATE TYPE "EtiquetaCaja" AS ENUM ('MANO', 'CUERPO', 'CARA', 'OBJETO');

-- CreateEnum
CREATE TYPE "TipoPuntosClave" AS ENUM ('MANO', 'CUERPO', 'CARA');

-- CreateEnum
CREATE TYPE "Dificultad" AS ENUM ('BASICO', 'INTERMEDIO', 'AVANZADO');

-- CreateEnum
CREATE TYPE "Calidad" AS ENUM ('PENDIENTE', 'BAJA', 'MEDIA', 'ALTA', 'EXCELENTE');

-- CreateEnum
CREATE TYPE "FuenteDatos" AS ENUM ('MANUAL', 'LOTE', 'GENERADO', 'EXTERNO');

-- CreateEnum
CREATE TYPE "TipoEtiqueta" AS ENUM ('GENERAL', 'LINGUISTICO', 'TECNICO', 'DIFICULTAD');

-- CreateEnum
CREATE TYPE "EstadoLote" AS ENUM ('PENDIENTE', 'PROCESANDO', 'COMPLETADO', 'FALLIDO', 'CANCELADO');

-- DropForeignKey
ALTER TABLE "BoundingBox" DROP CONSTRAINT "BoundingBox_sampleId_fkey";

-- DropForeignKey
ALTER TABLE "Category" DROP CONSTRAINT "Category_parentId_fkey";

-- DropForeignKey
ALTER TABLE "KeypointSet" DROP CONSTRAINT "KeypointSet_sampleId_fkey";

-- DropForeignKey
ALTER TABLE "Sample" DROP CONSTRAINT "Sample_signId_fkey";

-- DropForeignKey
ALTER TABLE "Sample" DROP CONSTRAINT "Sample_uploadBatchId_fkey";

-- DropForeignKey
ALTER TABLE "SampleMeta" DROP CONSTRAINT "SampleMeta_sampleId_fkey";

-- DropForeignKey
ALTER TABLE "Sign" DROP CONSTRAINT "Sign_categoryId_fkey";

-- DropForeignKey
ALTER TABLE "SignTag" DROP CONSTRAINT "SignTag_signId_fkey";

-- DropForeignKey
ALTER TABLE "SignTag" DROP CONSTRAINT "SignTag_tagId_fkey";

-- DropTable
DROP TABLE "BoundingBox";

-- DropTable
DROP TABLE "Category";

-- DropTable
DROP TABLE "KeypointSet";

-- DropTable
DROP TABLE "Sample";

-- DropTable
DROP TABLE "SampleMeta";

-- DropTable
DROP TABLE "Sign";

-- DropTable
DROP TABLE "SignTag";

-- DropTable
DROP TABLE "Tag";

-- DropTable
DROP TABLE "UploadBatch";

-- DropEnum
DROP TYPE "BatchStatus";

-- DropEnum
DROP TYPE "BoxLabel";

-- DropEnum
DROP TYPE "DataSource";

-- DropEnum
DROP TYPE "Difficulty";

-- DropEnum
DROP TYPE "KeypointType";

-- DropEnum
DROP TYPE "Quality";

-- DropEnum
DROP TYPE "SampleType";

-- DropEnum
DROP TYPE "TagType";

-- CreateTable
CREATE TABLE "Categoria" (
    "id" SERIAL NOT NULL,
    "codigo" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "descripcion" TEXT,
    "orden" INTEGER NOT NULL DEFAULT 0,
    "padreId" INTEGER,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizadoEn" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Categoria_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Sena" (
    "id" SERIAL NOT NULL,
    "codigo" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "descripcion" TEXT,
    "dificultad" "Dificultad" NOT NULL DEFAULT 'BASICO',
    "activa" BOOLEAN NOT NULL DEFAULT true,
    "categoriaId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizadoEn" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Sena_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Etiqueta" (
    "id" SERIAL NOT NULL,
    "nombre" TEXT NOT NULL,
    "tipo" "TipoEtiqueta" NOT NULL DEFAULT 'GENERAL',
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Etiqueta_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SenaEtiqueta" (
    "senaId" INTEGER NOT NULL,
    "etiquetaId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "SenaEtiqueta_pkey" PRIMARY KEY ("senaId","etiquetaId")
);

-- CreateTable
CREATE TABLE "Muestra" (
    "id" SERIAL NOT NULL,
    "tipo" "TipoMuestra" NOT NULL,
    "rutaArchivo" TEXT NOT NULL,
    "nombreOriginal" TEXT,
    "tamanoArchivo" INTEGER,
    "ancho" INTEGER,
    "alto" INTEGER,
    "fps" INTEGER,
    "duracion" DOUBLE PRECISION,
    "formato" TEXT,
    "calidad" "Calidad" NOT NULL DEFAULT 'PENDIENTE',
    "validada" BOOLEAN NOT NULL DEFAULT false,
    "validadaPor" TEXT,
    "validadaEn" TIMESTAMP(3),
    "fuente" "FuenteDatos" NOT NULL DEFAULT 'MANUAL',
    "loteSubidaId" TEXT,
    "senaId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizadoEn" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Muestra_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CajaDelimitadora" (
    "id" SERIAL NOT NULL,
    "x" DOUBLE PRECISION NOT NULL,
    "y" DOUBLE PRECISION NOT NULL,
    "ancho" DOUBLE PRECISION NOT NULL,
    "alto" DOUBLE PRECISION NOT NULL,
    "etiqueta" "EtiquetaCaja" NOT NULL,
    "confianza" DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    "muestraId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "CajaDelimitadora_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ConjuntoPuntosClaves" (
    "id" SERIAL NOT NULL,
    "tipo" "TipoPuntosClave" NOT NULL,
    "datos" JSONB NOT NULL,
    "confianza" DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    "muestraId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ConjuntoPuntosClaves_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "MetadatoMuestra" (
    "id" SERIAL NOT NULL,
    "clave" TEXT NOT NULL,
    "valor" TEXT NOT NULL,
    "muestraId" INTEGER NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "MetadatoMuestra_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "LoteSubida" (
    "id" TEXT NOT NULL,
    "nombre" TEXT,
    "descripcion" TEXT,
    "totalArchivos" INTEGER NOT NULL DEFAULT 0,
    "procesados" INTEGER NOT NULL DEFAULT 0,
    "exitosos" INTEGER NOT NULL DEFAULT 0,
    "fallidos" INTEGER NOT NULL DEFAULT 0,
    "estado" "EstadoLote" NOT NULL DEFAULT 'PENDIENTE',
    "categoriaObjetivoId" INTEGER,
    "autoValidar" BOOLEAN NOT NULL DEFAULT false,
    "errores" TEXT,
    "iniciadoEn" TIMESTAMP(3),
    "completadoEn" TIMESTAMP(3),
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizadoEn" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LoteSubida_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Categoria_codigo_key" ON "Categoria"("codigo");

-- CreateIndex
CREATE INDEX "Categoria_padreId_idx" ON "Categoria"("padreId");

-- CreateIndex
CREATE INDEX "Categoria_codigo_idx" ON "Categoria"("codigo");

-- CreateIndex
CREATE UNIQUE INDEX "Sena_codigo_key" ON "Sena"("codigo");

-- CreateIndex
CREATE INDEX "Sena_categoriaId_idx" ON "Sena"("categoriaId");

-- CreateIndex
CREATE INDEX "Sena_codigo_idx" ON "Sena"("codigo");

-- CreateIndex
CREATE INDEX "Sena_dificultad_idx" ON "Sena"("dificultad");

-- CreateIndex
CREATE UNIQUE INDEX "Etiqueta_nombre_key" ON "Etiqueta"("nombre");

-- CreateIndex
CREATE INDEX "Muestra_senaId_tipo_idx" ON "Muestra"("senaId", "tipo");

-- CreateIndex
CREATE INDEX "Muestra_calidad_idx" ON "Muestra"("calidad");

-- CreateIndex
CREATE INDEX "Muestra_loteSubidaId_idx" ON "Muestra"("loteSubidaId");

-- CreateIndex
CREATE INDEX "Muestra_creadoEn_idx" ON "Muestra"("creadoEn");

-- CreateIndex
CREATE INDEX "Muestra_senaId_calidad_tipo_idx" ON "Muestra"("senaId", "calidad", "tipo");

-- CreateIndex
CREATE INDEX "CajaDelimitadora_muestraId_idx" ON "CajaDelimitadora"("muestraId");

-- CreateIndex
CREATE INDEX "ConjuntoPuntosClaves_muestraId_tipo_idx" ON "ConjuntoPuntosClaves"("muestraId", "tipo");

-- CreateIndex
CREATE INDEX "MetadatoMuestra_muestraId_clave_idx" ON "MetadatoMuestra"("muestraId", "clave");

-- CreateIndex
CREATE INDEX "LoteSubida_estado_idx" ON "LoteSubida"("estado");

-- CreateIndex
CREATE INDEX "LoteSubida_creadoEn_idx" ON "LoteSubida"("creadoEn");

-- AddForeignKey
ALTER TABLE "Categoria" ADD CONSTRAINT "Categoria_padreId_fkey" FOREIGN KEY ("padreId") REFERENCES "Categoria"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sena" ADD CONSTRAINT "Sena_categoriaId_fkey" FOREIGN KEY ("categoriaId") REFERENCES "Categoria"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SenaEtiqueta" ADD CONSTRAINT "SenaEtiqueta_senaId_fkey" FOREIGN KEY ("senaId") REFERENCES "Sena"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SenaEtiqueta" ADD CONSTRAINT "SenaEtiqueta_etiquetaId_fkey" FOREIGN KEY ("etiquetaId") REFERENCES "Etiqueta"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Muestra" ADD CONSTRAINT "Muestra_loteSubidaId_fkey" FOREIGN KEY ("loteSubidaId") REFERENCES "LoteSubida"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Muestra" ADD CONSTRAINT "Muestra_senaId_fkey" FOREIGN KEY ("senaId") REFERENCES "Sena"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CajaDelimitadora" ADD CONSTRAINT "CajaDelimitadora_muestraId_fkey" FOREIGN KEY ("muestraId") REFERENCES "Muestra"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ConjuntoPuntosClaves" ADD CONSTRAINT "ConjuntoPuntosClaves_muestraId_fkey" FOREIGN KEY ("muestraId") REFERENCES "Muestra"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "MetadatoMuestra" ADD CONSTRAINT "MetadatoMuestra_muestraId_fkey" FOREIGN KEY ("muestraId") REFERENCES "Muestra"("id") ON DELETE CASCADE ON UPDATE CASCADE;
