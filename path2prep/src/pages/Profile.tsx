import React, { useEffect, useState, useRef } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchProfile, updateProfile, uploadProfilePicture, clearUpdateStatus } from '../store/slices/profileSlice';
import { Profile } from '../types';
import apiService from '../services/api';

const ProfilePage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { profile, loading, updating, updateSuccess, updateError } = useAppSelector((state) => state.profile);
  const { user } = useAppSelector((state) => state.auth);
  const [formData, setFormData] = useState<Partial<Profile>>({});
  const [picturePreview, setPicturePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Tag input state
  const [techInput, setTechInput] = useState('');
  const [softInput, setSoftInput] = useState('');
  const [interestInput, setInterestInput] = useState('');

  // Dropdown options from backend
  const [majorOptions, setMajorOptions] = useState<{ id: number; name: string }[]>([]);
  const [countryOptions, setCountryOptions] = useState<{ id: number; name: string }[]>([]);

  useEffect(() => {
    dispatch(fetchProfile());
    // Fetch dropdown options
    apiService.getMajorOptions().then(setMajorOptions).catch(() => { });
    apiService.getCountryOptions().then(setCountryOptions).catch(() => { });
  }, [dispatch]);

  useEffect(() => {
    if (profile) {
      setFormData(profile);
    }
  }, [profile]);

  // Auto-dismiss toast after 4 seconds
  useEffect(() => {
    if (updateSuccess || updateError) {
      const timer = setTimeout(() => {
        dispatch(clearUpdateStatus());
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [updateSuccess, updateError, dispatch]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      setFormData({ ...formData, [name]: (e.target as HTMLInputElement).checked });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handlePictureClick = () => {
    fileInputRef.current?.click();
  };

  const handlePictureChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Preview
      const reader = new FileReader();
      reader.onloadend = () => setPicturePreview(reader.result as string);
      reader.readAsDataURL(file);
      // Upload
      dispatch(uploadProfilePicture(file));
    }
  };

  const handleAddTag = (field: 'technical_skills' | 'soft_skills' | 'interests', value: string, setter: (v: string) => void) => {
    const trimmed = value.trim();
    if (trimmed && !(formData[field] as string[] || []).includes(trimmed)) {
      setFormData({
        ...formData,
        [field]: [...(formData[field] as string[] || []), trimmed],
      });
      setter('');
    }
  };

  const handleRemoveTag = (field: 'technical_skills' | 'soft_skills' | 'interests', index: number) => {
    const current = (formData[field] as string[] || []);
    setFormData({
      ...formData,
      [field]: current.filter((_, i) => i !== index),
    });
  };

  const handleTagKeyDown = (e: React.KeyboardEvent, field: 'technical_skills' | 'soft_skills' | 'interests', value: string, setter: (v: string) => void) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      handleAddTag(field, value, setter);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Strip out profile_picture from the JSON update (handled separately)
    const { profile_picture, id, user: userId, ...updateData } = formData as any;
    await dispatch(updateProfile(updateData));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-500 font-medium">Loading your profile...</p>
        </div>
      </div>
    );
  }

  const avatarUrl = picturePreview || (profile?.profile_picture ? `${profile.profile_picture}` : null);
  const initials = user?.full_name
    ? user.full_name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    : user?.email?.charAt(0).toUpperCase() || '?';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8 px-4">
      {/* Toast Notifications */}
      {updateSuccess && (
        <div className="fixed top-6 right-6 z-50 animate-slide-in">
          <div className="flex items-center gap-3 bg-emerald-500 text-white px-5 py-3 rounded-xl shadow-lg shadow-emerald-500/25">
            <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="font-medium">Profile updated successfully!</span>
            <button onClick={() => dispatch(clearUpdateStatus())} className="ml-2 hover:opacity-75">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}
      {updateError && (
        <div className="fixed top-6 right-6 z-50 animate-slide-in">
          <div className="flex items-center gap-3 bg-red-500 text-white px-5 py-3 rounded-xl shadow-lg shadow-red-500/25">
            <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <span className="font-medium">Failed to update profile</span>
              <p className="text-sm text-red-100">{updateError}</p>
            </div>
            <button onClick={() => dispatch(clearUpdateStatus())} className="ml-2 hover:opacity-75">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mb-6">
          <div className="flex items-center gap-6">
            {/* Avatar */}
            <div className="relative group cursor-pointer" onClick={handlePictureClick}>
              {avatarUrl ? (
                <img
                  src={avatarUrl}
                  alt="Profile"
                  className="w-24 h-24 rounded-full object-cover ring-4 ring-blue-100 transition-all group-hover:ring-blue-300"
                />
              ) : (
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center ring-4 ring-blue-100 transition-all group-hover:ring-blue-300">
                  <span className="text-white text-2xl font-bold">{initials}</span>
                </div>
              )}
              <div className="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handlePictureChange}
              />
            </div>
            {/* Name & Email */}
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-slate-800">
                {user?.full_name || user?.username || 'Your Profile'}
              </h1>
              <p className="text-slate-500 mt-1">{user?.email}</p>
              <p className="text-xs text-slate-400 mt-1">Click the avatar to change your profile picture</p>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Academic Information */}
          <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14l9-5-9-5-9 5 9 5z" />
                  <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5zM12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zM12 14v7" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-slate-800">Academic Information</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">GPA</label>
                <input type="number" step="0.01" min="0" max="4" name="gpa" value={formData.gpa ?? ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="e.g. 3.75" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Degree Level</label>
                <select name="degree_level" value={formData.degree_level || ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
                  <option value="">Select degree level</option>
                  <option value="High School">High School</option>
                  <option value="Bachelor's">Bachelor's</option>
                  <option value="Master's">Master's</option>
                  <option value="PhD">PhD</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Major / Field of Study</label>
                <select name="major" value={formData.major || ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
                  <option value="">Select major</option>
                  {majorOptions.map((opt) => (
                    <option key={opt.id} value={opt.name}>{opt.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Country</label>
                <select name="country" value={formData.country || ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
                  <option value="">Select country</option>
                  {countryOptions.map((opt) => (
                    <option key={opt.id} value={opt.name}>{opt.name}</option>
                  ))}
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Target Country</label>
                <select name="target_country" value={formData.target_country || ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
                  <option value="">Select target country</option>
                  {countryOptions.map((opt) => (
                    <option key={opt.id} value={opt.name}>{opt.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </section>

          {/* Test Scores */}
          <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center">
                <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-slate-800">Test Scores</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">IELTS</label>
                <input type="number" step="0.5" min="0" max="9" name="ielts_score" value={formData.ielts_score ?? ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="0 - 9" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">TOEFL</label>
                <input type="number" min="0" max="120" name="toefl_score" value={formData.toefl_score ?? ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="0 - 120" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">GRE</label>
                <input type="number" min="260" max="340" name="gre_score" value={formData.gre_score ?? ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="260 - 340" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">GMAT</label>
                <input type="number" min="200" max="800" name="gmat_score" value={formData.gmat_score ?? ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="200 - 800" />
              </div>
            </div>
          </section>

          {/* Financial Information */}
          <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center">
                <svg className="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-slate-800">Financial Information</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Income Range</label>
                <select name="income_range" value={formData.income_range || ''} onChange={handleChange}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition">
                  <option value="">Select income range</option>
                  <option value="below_20k">Below $20,000</option>
                  <option value="20k_40k">$20,000 – $40,000</option>
                  <option value="40k_60k">$40,000 – $60,000</option>
                  <option value="60k_80k">$60,000 – $80,000</option>
                  <option value="80k_100k">$80,000 – $100,000</option>
                  <option value="above_100k">Above $100,000</option>
                </select>
              </div>
              <div className="flex items-center gap-3 pt-6">
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    name="need_based_preference"
                    checked={formData.need_based_preference || false}
                    onChange={handleChange}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-100 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
                <span className="text-sm font-medium text-slate-600">I prefer need-based scholarships</span>
              </div>
            </div>
          </section>

          {/* Skills & Interests */}
          <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-slate-800">Skills & Interests</h2>
            </div>
            <div className="space-y-5">
              {/* Technical Skills */}
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Technical Skills</label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {(formData.technical_skills || []).map((skill, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium">
                      {skill}
                      <button type="button" onClick={() => handleRemoveTag('technical_skills', i)} className="hover:text-blue-900">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                      </button>
                    </span>
                  ))}
                </div>
                <input type="text" value={techInput} onChange={(e) => setTechInput(e.target.value)}
                  onKeyDown={(e) => handleTagKeyDown(e, 'technical_skills', techInput, setTechInput)}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="Type a skill and press Enter (e.g. Python, React)" />
              </div>
              {/* Soft Skills */}
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Soft Skills</label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {(formData.soft_skills || []).map((skill, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full text-sm font-medium">
                      {skill}
                      <button type="button" onClick={() => handleRemoveTag('soft_skills', i)} className="hover:text-emerald-900">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                      </button>
                    </span>
                  ))}
                </div>
                <input type="text" value={softInput} onChange={(e) => setSoftInput(e.target.value)}
                  onKeyDown={(e) => handleTagKeyDown(e, 'soft_skills', softInput, setSoftInput)}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="Type a skill and press Enter (e.g. Leadership, Teamwork)" />
              </div>
              {/* Interests */}
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Interests</label>
                <div className="flex flex-wrap gap-2 mb-2">
                  {(formData.interests || []).map((interest, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-3 py-1 bg-amber-50 text-amber-700 rounded-full text-sm font-medium">
                      {interest}
                      <button type="button" onClick={() => handleRemoveTag('interests', i)} className="hover:text-amber-900">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                      </button>
                    </span>
                  ))}
                </div>
                <input type="text" value={interestInput} onChange={(e) => setInterestInput(e.target.value)}
                  onKeyDown={(e) => handleTagKeyDown(e, 'interests', interestInput, setInterestInput)}
                  className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="Type an interest and press Enter (e.g. AI, Music)" />
              </div>
            </div>
          </section>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={updating}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/25"
            >
              {updating ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Save Profile
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Toast slide-in animation */}
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        .animate-slide-in {
          animation: slideIn 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default ProfilePage;
