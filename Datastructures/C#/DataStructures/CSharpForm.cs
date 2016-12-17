using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using System.Xml.Serialization;

namespace DataStructures
{
    public partial class CSharpForm : Form
    {

        private Person[] Persons = new Person[3];
        private List<Person> PersonatList = new List<Person>();
        private Dictionary<Person, Book> Library;
        private LibraryDict libDict = new LibraryDict();
        private LinkedList<Person> personsLinkedList = new LinkedList<Person>();
        private Person p1;
        private Person p2;
        private Person p3;
        private Person p4;
        private Person p5;
        private Book b1;
        private Book b2;

        private StringBuilder sb = new StringBuilder();
        private StringBuilder sb2 = new StringBuilder();

        public CSharpForm()
        {
            InitializeComponent();
            /// deklarimi objekteve të tipit Person 
            p1 = new Person("Ahmet", "Murati", "Mashkull", new DateTime(1979, 04, 29));
            p2 = new Person("Ridvan", "Bunjaku", "Mashkull", DateTime.Now);
            p3 = new Person("Ridvan", "Aliu", "Mashkull", DateTime.Now);
            p4 = new Person("Erzen", "Komoni", "Mashkull", DateTime.Now);
            p5 = new Person("Fitim", "Bejtullahu", "Mashkull", DateTime.Now);

            b1 = new Book("Kronikë në gur", "Ismail Kadare", "1233445432");
            b2 = new Book("Sikur të isha djalë!", "Haki Stërmilli", "12323212223");

            Library = new Dictionary<Person, Book>();

            /// Inicializimi i elementeve të vargut të tipit Array
            for (int i = 0; i < Persons.Length; i++)
            {
                Persons[i] = new Person();
            }

            Persons[0] = p1;
            Persons[1] = p2;
            Persons[2] = p3;
            // Persons[3] = p4;
            int k = 0;
            //for (int i = 0; i < this.Persons.Length; i++)
            //{
            //    sb.AppendLine((k++) + ". " + this.Persons[i].ToString());
            //}
            foreach (var item in Persons)
            {
                sb.AppendLine((++k) + ". " + item.ToString());
            }


            Library.Add(p1, b2);
           //  Library.Add(p1, b2);
             Library.Add(p2, b1);


            sb.AppendLine(libDict.AssingBook(p1, b1));
            sb.AppendLine(libDict.AssingBook(p1, b1));
            sb.AppendLine(libDict.AssingBook(p2, b2));
            sb.AppendLine(libDict.AssingBook(p1, b1));


            PersonatList.Add(p1);
            PersonatList.Add(p2);
            PersonatList.Add(p3);
            PersonatList.Add(p4);
            PersonatList.Add(p5);
            sb.AppendLine("Data from Generics Persons").AppendLine();
            int o = 0;
            foreach (Person p in this.PersonatList)
            {
                sb.AppendFormat("The person with name {0} {1} born on {2} {3:N2} {3:C2}", p.Firstname, p.Lastname, p.Birthday, ++o).AppendLine(); 
            }
            sb.AppendLine();
            sb2.AppendLine();

            sb2.AppendLine("First element");
            personsLinkedList.AddFirst(p5);
            foreach (Person p3a in personsLinkedList)
            {
                sb2.AppendLine(p3a.ToString());
            }
            sb2.AppendLine().AppendLine();
            sb2.AppendLine("Second element");
            personsLinkedList.AddAfter(personsLinkedList.First, p3);
            foreach (Person p3a in personsLinkedList)
            {
                sb2.AppendLine(p3a.ToString());
            }
            sb2.AppendLine().AppendLine();
            sb2.AppendLine("Third element");
            personsLinkedList.AddBefore(personsLinkedList.First, p2);
            foreach (Person p3a in personsLinkedList)
            {
                sb2.AppendLine(p3a.ToString());
            }
            sb2.AppendLine().AppendLine();
            sb2.AppendLine("Fourth Element");
            personsLinkedList.AddLast(p1);
            foreach (Person p3a in personsLinkedList)
            {
                sb2.AppendLine(p3a.ToString());
            }

            sb.AppendLine().AppendLine().AppendLine(sb2.ToString());

            textBox1.Text = (sb.ToString());
        }

        private void tssmiSaveJSON_Click(object sender, EventArgs e)
        {
            string path = Application.StartupPath;
            if (String.IsNullOrEmpty(path))
            {
                path = System.IO.Path.GetDirectoryName(System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName);
            }
            using (JsonTextWriter tw = new JsonTextWriter(new StreamWriter(Path.Combine(path, "PersonList.json"))))
            {
                tw.Formatting = Newtonsoft.Json.Formatting.Indented;
                String json = JsonConvert.SerializeObject(this.PersonatList);
                tw.WriteRaw(json);
                tw.Flush();
                tw.CloseOutput = true;
            }
        }

        private void tsmiLoadJSON_Click(object sender, EventArgs e)
        {
            string path = Application.StartupPath;
            if (String.IsNullOrEmpty(path))
            {
                path = System.IO.Path.GetDirectoryName(System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName);
            }
            using (TextReader tr = new StreamReader(Path.Combine(path, "PersonList.json")))
            {
                String json = tr.ReadToEnd();

                this.PersonatList = (List<Person>)JsonConvert.DeserializeObject<List<Person>>(json);
                PopulatePersonatList();
            }
        }

        private void PopulatePersonatList()
        {
            StringBuilder sb = new StringBuilder();
            foreach (Person p3a in PersonatList)
            {

                sb.AppendLine(p3a.ToString());
            }

            textBox1.Text = sb.ToString();
        }

        private void tsmiSaveXML_Click(object sender, EventArgs e)
        {
            string path = Application.StartupPath;
            if (String.IsNullOrEmpty(path))
            {
                path = System.IO.Path.GetDirectoryName(System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName);
            }
            System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(this.PersonatList.GetType());

            System.IO.StreamWriter file = new System.IO.StreamWriter(Path.Combine(path, "PersonatList.xml"));
            x.Serialize(file, PersonatList);
            file.Close();
        }

        private void tsmiLoadXML_Click(object sender, EventArgs e)
        {
            string path = Application.StartupPath;
            if (String.IsNullOrEmpty(path))
            {
                path = System.IO.Path.GetDirectoryName(System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName);
            }
            XmlTextReader reader = new XmlTextReader(Path.Combine(path, "PersonatList.xml"));
            // of object that is being deserialized.
            XmlSerializer mySerializer =
            new XmlSerializer(typeof(List<Person>));
            // To read the file, create a FileStream.
            FileStream myFileStream =
            new FileStream(Path.Combine(path, "PersonatList.xml"), FileMode.Open);
            // Call the Deserialize method and cast to the object type.
            this.PersonatList = (List<Person>) mySerializer.Deserialize(myFileStream);
            PopulatePersonatList();
        }


    }

    public class LibraryDict : Dictionary<Person, Book>
    {
        internal bool AddLending(Person p, Book b)
        {
            Book l2 = new Book();
            bool res = this.TryGetValue(p, out l2);
            res = b.Equals(l2);
            if (!res)
            {
                this.Add(p, b);
                res = true;
            }
            else
            {
                res = false;
            }
            return res;
        }

        internal string AssingBook(Person p, Book b)
        {
            String str = ("Trying to assign the book " + b.ToString() + " to the person " + p.ToString());
            if (this.AddLending(p, b))
            {
                str += ("\nThe book " + b.ToString() + " is assigned to the person " + p.ToString());
            }
            else
            {
                str += ("\nThe book " + b.ToString() + " is not assigned to the person " + p.ToString());
            }
            return (str);
        }

    }

    public class Book
    {
        public Book()
        {
            this.Title = "";
            this.Author = "";
            this.ISBN = "";
        }

        public Book(string _title, string _author, string _isbn)
        {
            this.Title = _title;
            this.Author = _author;
            this.ISBN = _isbn;
        }

        public string Title { get; set; }
        public String Author { get; set; }
        public String ISBN { get; set; }

        public override string ToString()
        {
            return Author + " - \"" + Title + "\"";
        }

        public override bool Equals(object obj)
        {
            if (obj is Book)
            {
                Book tjetra = (Book)obj;
                return this.ISBN.Equals(tjetra.ISBN);
            }
            return false;
        }
    }

    public class Person
    {

        public Person()
        {
            this.Firstname = "";
            this.Lastname = "";
            this.Sex = "";
            this.Birthday = DateTime.MinValue;
        }

        public Person(string _firstname, string _lastname, string _sex, DateTime _birthday)
            : base()
        {
            // TODO: Complete member initialization
            this.Firstname = _firstname;
            this.Lastname = _lastname;
            this.Sex = _sex;
            this.Birthday = _birthday;
        }

        public String Firstname { get; set; }
        public String Lastname { get; set; }
        public String Sex { get; set; }
        public DateTime Birthday { get; set; }

        public override string ToString()
        {
            return Firstname + " " + Lastname;
        }

        public override bool Equals(object obj)
        {
            if (obj is Person)
            {
                Person tjetra = (Person)obj;
                return this.Firstname.Equals(tjetra.Firstname) && this.Lastname.Equals(tjetra.Lastname);
            }
            return false;
        }

    }
}
