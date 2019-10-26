﻿// <auto-generated />
using System;
using HackathonBase.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace HackathonBase.Migrations
{
    [DbContext(typeof(EntryContext))]
    [Migration("20191025232847_entryMigration1")]
    partial class entryMigration1
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "2.1.11-servicing-32099")
                .HasAnnotation("Relational:MaxIdentifierLength", 128)
                .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

            modelBuilder.Entity("HackathonBase.Models.Device", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

                    b.Property<string>("Name");

                    b.HasKey("Id");

                    b.ToTable("Device");
                });

            modelBuilder.Entity("HackathonBase.Models.Entry", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

                    b.Property<float>("Average");

                    b.Property<DateTime>("EndTime");

                    b.Property<int?>("SourceDeviceId");

                    b.Property<DateTime>("StartTime");

                    b.HasKey("Id");

                    b.HasIndex("SourceDeviceId");

                    b.ToTable("Entries");
                });

            modelBuilder.Entity("HackathonBase.Models.Entry", b =>
                {
                    b.HasOne("HackathonBase.Models.Device", "SourceDevice")
                        .WithMany()
                        .HasForeignKey("SourceDeviceId");
                });
#pragma warning restore 612, 618
        }
    }
}
