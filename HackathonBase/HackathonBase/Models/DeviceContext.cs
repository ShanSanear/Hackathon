using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace HackathonBase.Models
{
    public class DeviceContext : DbContext
    {
        public DbSet<Device> Devices { get; set; }

        public DeviceContext(DbContextOptions options) : base(options)
        {

        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Device>().HasKey(x => x.Id);
        }
    }
}
