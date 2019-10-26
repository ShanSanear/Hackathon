using Microsoft.EntityFrameworkCore;

namespace HackathonBase.Models
{
    public class EntryContext : DbContext
    {
        public DbSet<Entry> Entries { get; set; }

        public EntryContext(DbContextOptions options) : base(options)
        {

        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Entry>().HasKey(x => x.Id);
        }
    }
}
